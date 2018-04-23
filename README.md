# Jupyter Notebook Viewer

## Overview
Fetches and displays part of, or an entire Jupyter Notebook in an XBlock.

## Installation
### XBlock
* login as the root user: `sudo -i`
* New Installation:
    * `/edx/bin/pip.edxapp install git+https://gitlab.com/iblstudios/jupyter-viewer-xblock.git`
* Re-Installation:
    * `/edx/bin/pip.edxapp install --upgrade --no-deps --force-reinstall git+https://gitlab.com/iblstudios/jupyter-viewer-xblock.git`
* Restart the `edxapp` via `/edx/bin/supervisorctl restart edxapp:`

### Edx Server Setup
* In the studio, go to the course you would like to implement this XBlock in
* Under `Settings` at the top, select `Advanced Settings`
* in the Advanced Module List, add: `"xblock_jupyter_viewer"`
    * ensure there is a comma after the second to last entry, and no comma exists after the last entry
* Select Save

The viewer can now be added to a unit by selecting `Jupyter Notebook Viewer` from the `Advanced` component menu

### LMS/CMS Setup
In the following two files:
* `/edx/app/edxapp/edx-platform/lms/urls.py` 
* `/edx/app/edxapp/edx-platform/cms/urls.py` 

Add the following to the bottom of each file:
```python
# Jupyter Viewer XBlock Endpoint
urlpatterns += (
    url(r'^api/jupyter/', include('xblock_jupyter_viewer.rest.urls')),
)
```

In the following files:
* `/edx/app/edxapp/edx-platform/lms/envs/common.py` 
* `/edx/app/edxapp/edx-platform/cms/envs/common.py` 

Add the following at the bottom of the `INSTALLED_APPS` section:
```python
    # Jupyter Notebook Viewer XBlock
    'xblock_jupyter_viewer',
```

Restart `edxapp` via `/edx/bin/supervisorctl restart edxapp:`

## How it works
The XBlock contains an `iframe` that points to the REST endpoint.

The REST endpoint takes the following query parameters:
* `url`: URL to the **RAW** jupyter notebook JSON file
* `start`: (optional) text that starting cell contains
    * if supplied, will start in **FIRST** cell that contains this text
    * if not supplied, it starts at the beginning
* `end`: (optional) text that ending cell contains
    * if supplied, will end at **FIRST** cell that contains this text (not-inclusive)
    * if not supplied, it will end at the end of the document

It is often easiest to use the markdown headers as the start/end tags, eg:
* `### My Start Header`

If either start/end tags cannot be found in the document, they are ignored.

The REST endpoint returns the entire HTML + embedded CSS in order to be rendered in the XBlock iframe.

The user can also set the height of the XBlock in pixels in the Studio.

## Pre/Post Processors
There are various pre and post processors that are applied to notebook when converting it to the final HTML.

### Pre-Processors
These operate on each cell of the notebook, typically making some kind of change to either the overall notebook structure or a single cell.

The cells of the notebook are iterated over and each cell is passed to one of the processors, in the sequence the processors are added. 

After all cells have completed, the `finish` function is called for each processor to do any final cleanup.

New pre-processors can be added by subclassing `preprocessors.Processor` and appending an instance of it to the `transforms` list.

### Post-Processors
These operate on the final, raw HTML output string, making modifications as necessary. 

New post processors can be added in the `postprocess` function
