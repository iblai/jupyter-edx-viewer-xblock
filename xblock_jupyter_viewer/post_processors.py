import logging 
import re

log = logging.getLogger(__name__)


def remove_box_shadow(raw_html):
    """Removes box shadow around document by replacing defining class name"""
    container = "#notebook-container"
    log.debug("Found #notebook-container class: {}".format(raw_html.find(container)))

    return raw_html.replace(container, "#doesnotexisthere")


def insert_target_blank(raw_html):
    """Adds 'target=_blank' attribute to all `<a href=...>` links """
    return re.sub('(<a .+?>)', _match_fn, raw_html)


def _match_fn(matchobj):
    """Return original <a href...> with `target='_blank'` inserted"""
    s = matchobj.group(0)
    return '{} target="_blank" {}'.format(s[:2], s[3:])
