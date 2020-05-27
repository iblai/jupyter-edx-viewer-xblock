"""Jupyter Notebook Viewer XBlock"""

import logging
import pkg_resources
from urllib.parse import urlencode

from django.core.urlresolvers import reverse

from xblock.core import XBlock
from xblock.fields import Scope, String, Integer
from xblock.fragment import Fragment
from xblockutils.studio_editable import StudioEditableXBlockMixin

log = logging.getLogger(__name__)


class JupyterViewerXBlock(XBlock, StudioEditableXBlockMixin):
    """iframe used with endpoint to render full/section of jupyter notebook"""

    display_name = String(
        display_name="Display Name", default="Jupyter Notebook Viewer",
        scope=Scope.settings,
        help="Name of this XBlock" 
    )

    jupyter_url = String(
        help="URL to the .ipynb File",
        scope=Scope.content,
        display_name="Notebook URL",
        default="http://path/to/file.ipynb"
    )

    image_url = String(
        help="(Optional) Absolute URL to images root (http://.../)",
        scope=Scope.content,
        display_name="Image Root URL",
        default=""
    )

    start_tag = String(
        help="(Optional) Finds first occurrence of this text and renders notebook starting in this cell",
        scope=Scope.content,
        display_name="Start Tag",
        default=""
    )

    end_tag = String(
        help="(Optional) Finds first occurrence of this text and renders notebook up to this cell (not inclusive)",
        scope=Scope.content,
        display_name="End Tag",
        default=""
    )

    xblock_height = Integer(
        help="Height of this XBlock (px)",
        scope=Scope.content,
        display_name="Height",
        default=500
    )

    editable_fields = ('display_name', 'jupyter_url', 'image_url', 'start_tag', 'end_tag', 'xblock_height')

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def student_view(self, context=None):
        base = reverse('xblock_jupyter_viewer:jupyter_nb_viewer') + "?{}"

        # setup start/end tags
        if self.start_tag != '':
            base += "&{}".format(urlencode({'start': self.start_tag}))
        if self.end_tag != '':
            base += "&{}".format(urlencode({'end': self.end_tag}))
        # Add Image root
        base += "&{}".format(urlencode({'images_url': self.image_url}))

        # setup full url and inject into template iframe
        full_url = base.format(urlencode({'url': self.jupyter_url}))
        log.debug("Full URL: {}".format(full_url))
        base_html = self.resource_string('static/html/student_view.html')\
            .format(self.xblock_height, full_url)
        
        # add html and css
        frag = Fragment(base_html)
        # frag.add_css(self.resource_string('static/css/style.css'))
        return frag

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("MyXBlock",
             """<myxblock/>
             """),
            ("Multiple MyXBlock",
             """<vertical_demo>
                <myxblock/>
                <myxblock/>
                <myxblock/>
                </vertical_demo>
             """),
        ]

