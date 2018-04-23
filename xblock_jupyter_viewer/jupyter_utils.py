import json
import logging 

import requests
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError
from nbconvert import HTMLExporter

from preprocessors import ImageReplacement, RemoveCustomCSS
from post_processors import remove_box_shadow, insert_target_blank


log = logging.getLogger(__name__)


def fetch_notebook(url):
    """Fetches the notbook from URL"""

    log.info("Fetching URL: {}".format(url))
    resp = requests.get(url)
    return resp


def json_to_nb_format(nb_str):
    """Converts Notebook JSON to python object"""
    nb = nbformat.reads(nb_str, as_version=4)
    return nb


def convert_to_html(nb):
    """Converts notebook dict to HTML with included CSS"""
    exporter = HTMLExporter()
    body, resources = exporter.from_notebook_node(nb)

    return body, resources


def filter_start_end(nb, start_tag=None, end_tag=None):
    """Filter out everything outside of `start_tag` and `end_tag`"""

    # Just return if nothing to filter
    if start_tag is None and end_tag is None:
        return nb

    start_cell_num = 0
    num_cells = end_cell_num = len(nb['cells'])
    for cell_num, cell in enumerate(nb['cells']):
        # Find first occurrence of start_tag
        if start_tag and start_tag in cell['source'] and start_cell_num == 0:
            start_cell_num = cell_num
        # Find first occurrence of end_tag
        if end_tag and end_tag in cell['source'] and end_cell_num == num_cells:
            end_cell_num = cell_num

    if start_tag and start_cell_num == 0:
        log.warning("No cell with start content: {} found".format(start_tag))
    if end_tag and end_cell_num == num_cells:
        log.warning("No cell with start content: {} found".format(end_tag))

    nb['cells'] = nb['cells'][start_cell_num:end_cell_num]
    
    return nb


def preprocess(nb, processors):
    """Applies preprocessor to each cell"""
    gen = (cell for cell in nb['cells'])

    # Run processor on each cell
    for cell in gen:
        for t in processors:
            t.process_cell(cell)
    
    # Run finish on each processor
    for t in processors:
        t.finish()


def postprocess(raw_html):
    """Post-processes raw html"""
    html = remove_box_shadow(raw_html)
    html = insert_target_blank(html)
    return html


def process_nb(url, images_url=None, start=None, end=None):
    """Main method to fetch, process, and return HTML for ipython notebook"""

    # Retrieve nb from URL, conver to python fmt, and filter appropriately
    response = fetch_notebook(url)
    nb = json_to_nb_format(response.text)
    nb = filter_start_end(nb, start, end)

    # Setup pre-processors
    transforms = [RemoveCustomCSS(nb)]
    if images_url:
        transforms.append(ImageReplacement(nb, images_url))

    # Run transformation pipeline
    preprocess(nb, transforms)
    html, resources = convert_to_html(nb)
    html = postprocess(html)

    return html



