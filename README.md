# Jupyter Notebook Viewer

## Overview
_Fetch and display part of, or an entire Jupyter Notebook in an XBlock._

Jupyter is a "killer app" for education, said Prof. Lorena Barba in her [keynote](http://lorenabarba.com/gallery/prof-barba-gave-keynote-at-scipy-2014/) at the 2014 Scientific Python Conference ([video](https://youtu.be/TWxwKDT88GU?t=9m24s) available).
Many people are writing lessons, tutorials, whole courses and even books using Jupyter.
It is a **new genre of open educational resource** (OER).
What if you want to create an online course on Open edX using content originally written as Jupyter notebook?
You certainly don't want to duplicate the content, much less copy-and-paste.
This XBlock allows you to embed the content dynamically from a notebook available on a public URL.

Prof. Barba used the XBlock in the second half of her course module, [Get Data Off The Ground with Python](https://openedx.seas.gwu.edu/courses/course-v1:GW+EngComp1+2018/about).
Check it out!


## Installation
### XBlock
* login as the root user: `sudo -i`
* New Installation:
    * `/edx/bin/pip.edxapp install git+https://github.com/ibleducation/jupyter-viewer-xblock.git`
* Re-Installation:
    * `/edx/bin/pip.edxapp install --upgrade --no-deps --force-reinstall git+https://github.com/ibleducation/jupyter-viewer-xblock.git`
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
    * if supplied, will end at **FIRST** cell that contains this text (not-inclusive - this cell is not shown) 
    * if not supplied, it will end at the end of the document
* `images_url`: (optional) url to root of an images location (for `<img>` tags)
    * if supplied, this will be pre-pended to the filename in the `src` attribute of all `<img src=...>` tags in the notebook
    * example: 
        * images_url :`http://mysite.com/images/`
        * `<img src="/something/image.jpg">` becomes `<img src="http://mysite.com/images/image.jp">`

It is often easiest to use the markdown headers as the start/end tags, eg:
* `### My Start Header`

If either start/end tags cannot be found in the document, they are ignored.

The REST endpoint returns the entire HTML + embedded CSS in order to be rendered in the XBlock iframe.

The user can also set the height of the XBlock in pixels in the Studio.

## Pre/Post Processors
There are various pre and post processors that are applied to notebook when converting it to the final HTML.

### Pre-Processors
These operate on each cell of the notebook, typically making some kind of change to either the overall notebook structure or a single cell.

The cells of the notebook are iterated over and each cell is passed to each processor in the sequence the processors are added. 

After all cells have completed, the `finish` function is called for each processor to do any final cleanup.

New pre-processors can be added by subclassing `preprocessors.Processor` and appending an instance of it to the `transforms` list.

### Post-Processors
These operate on the final, raw HTML output string, making modifications as necessary. 

New post processors can be added in the `postprocess` function

## Copyright and License

(c) 2017 IBL Studios and Lorena A. Barba, [code is under BSD-3 clause](https://github.com/engineersCode/EngComp/blob/master/LICENSE). 

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

