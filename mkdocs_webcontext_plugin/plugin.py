import os
import sys
import re
import logging
from timeit import default_timer as timer
from datetime import datetime, timedelta

from mkdocs import utils as mkdocs_utils
from mkdocs.config import config_options, Config
from mkdocs.plugins import BasePlugin
from mkdocs.structure.pages import Page

from pathlib import Path

LOGGER = logging.getLogger(__name__)

class Webcontext(BasePlugin):

    config_scheme = (
        ('context', config_options.Type(str, default='/')),
    )

    md_link = re.compile(r'''(\[[^]]*]\()(/[^)]*)(\))|(\[[^]]*]:\s)(/[^\n\r)]*)''', re.DOTALL | re.UNICODE)      

    def __init__(self):
        self.enabled = True
        self.total_time = 0
    
    def on_page_markdown(self, markdown, page, config, files):
        context = self.config['context']
        new_md = self._absolute_to_webcontext(markdown, context)
        return new_md
    
    def _absolute_to_webcontext(self, markdown, context: str):
        LOGGER.debug('webcontext: using defined context = %s', context)

        def _check_link(link: str, context: str):
            contextLink = context +"/"+ link[1:]
            LOGGER.debug('webcontext: replace %s with %s', link, contextLink)
            link = link.replace(link[1:], contextLink)
            link = link.replace("\\", "/")

            return link

        def _to_webcontext(context:str):
            def re_write_link(matchobj):
                group1 = matchobj.group(1)  # front stuff
                group2 = matchobj.group(2)  # the actual link
                group3 = matchobj.group(3)  # closing tag

                if group1 and group2 and group3:
                    link = _check_link(group2, context)
                    return "{}{}{}".format(group1, link, group3)

                group4 = matchobj.group(4)  # front stuff
                group5 = matchobj.group(5)  # the actual link
                if group4 and group5:
                    link = _check_link(group5, context)
                    return "{}{}".format(group4, link)

            return re_write_link

        file_data = re.sub(self.md_link, _to_webcontext(context), markdown)
        return file_data