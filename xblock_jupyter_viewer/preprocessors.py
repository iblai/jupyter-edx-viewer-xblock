import logging
import re

log = logging.getLogger(__name__)


class Processor(object):
    """Base cell transformer - applies `process_cell` to each cell"""
    def __init__(self, nb):
        self.nb = nb

    def process_cell(self, cell):
        raise NotImplemented

    def finish(self):
        """Optional function to be called after iterations are complete"""
        pass


class RemoveCustomCSS(Processor):
    """Remove the cell that loads custom css if it's present"""

    def __init__(self, nb):
        super(RemoveCustomCSS, self).__init__(nb)
        self.search_text = 'from IPython.core.display import HTML'
        self.found = False
        self.cell_num = 0
    
    def process_cell(self, cell):
        if not self.found:
            if self.search_text in cell['source']:
                log.debug("Found Custom CSS Cell @ cells[{}]".format(self.cell_num))
                self.found = True
                return
            self.cell_num += 1 

    def finish(self):
        """Remove custom css cell if found"""
        if self.found:
            del self.nb['cells'][self.cell_num]
            log.debug("Removed cell #: {} [custom css]".format(self.cell_num))


class ImageReplacement(Processor):
    """Replaces img src attribute with absolute path"""
    
    def __init__(self, nb, images_url):
        super(ImageReplacement, self).__init__(nb)
        self.images_url = images_url

    def process_cell(self, cell):
        matches = re.findall(r'<img.+src=\"(.+?)\"', cell['source'])
        for m in matches:
            tail = m.split('/')[-1]
            cell['source'] = cell['source'].replace(m, '{}{}'.format(self.images_url, tail))
