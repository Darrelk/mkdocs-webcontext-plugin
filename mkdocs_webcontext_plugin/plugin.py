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
    md_link = re.compile(r'''(?P<full>(?P<prefix>!?\[[^\]]*\]\()(?P<url>/[^)]+)(?P<suffix>\)))|(?P<refprefix>\[[^\]]+\]:\s)(?P<refurl>/[^\s]+)''',re.DOTALL | re.UNICODE)
    html_src = re.compile(r'''(<img[^>]+src=["'])(/[^"'>]+)(["'])''', re.IGNORECASE)
    css_url_pattern = re.compile(r'''url\((["'])(/[^"')]+)(["'])\)''', re.IGNORECASE)

    def __init__(self):
        self.enabled = True
        self.total_time = 0
    
    def on_page_markdown(self, markdown, page, config, files):
        context = self.config['context']
        updated_md = self._rewrite_html_src(markdown, context)
        updated_md = self._absolute_to_webcontext(updated_md, context)
        return updated_md

    def _rewrite_html_src(self, html: str, context: str):
        def replace_src(match):
            prefix, path, suffix = match.groups()
            new_path = '/' + context.rstrip('/') + '/' + path.lstrip('/')
            new_path = new_path.replace("\\", "/")
            LOGGER.debug('webcontext: replace HTML src %s with %s', path, new_path)
            return f"{prefix}{new_path}{suffix}"

        return re.sub(self.html_src, replace_src, html)

    def _absolute_to_webcontext(self, markdown, context: str):
        LOGGER.debug('webcontext: using defined context = %s', context)

        def _check_link(link: str, context: str):
            contextLink = context +"/"+ link[1:]
            LOGGER.debug('webcontext: replace %s with %s', link, contextLink)
            link = link.replace(link[1:], contextLink)
            link = link.replace("\\", "/")

            return link

        def _to_webcontext(context: str):
          def re_write_link(match):
              if match.group('full'):
                  prefix = match.group('prefix')
                  url = match.group('url')
                  suffix = match.group('suffix')
                  new_url = _check_link(url, context)
                  return f"{prefix}{new_url}{suffix}"
              elif match.group('refprefix') and match.group('refurl'):
                  refprefix = match.group('refprefix')
                  refurl = match.group('refurl')
                  new_url = _check_link(refurl, context)
                  return f"{refprefix}{new_url}"
              return match.group(0)
          return re_write_link

        file_data = re.sub(self.md_link, _to_webcontext(context), markdown)
        return file_data

    def _process_css_file(self, file_path: Path, context: str):
        try:
            content = file_path.read_text(encoding="utf-8")

            def replace_url(match):
                quote1, path, quote2 = match.groups()
                new_path = '/' + context.strip('/') + '/' + path.lstrip('/')
                new_path = new_path.replace("\\", "/")
                LOGGER.debug("webcontext: replace CSS url %s with %s", path, new_path)
                return f"url({quote1}{new_path}{quote2})"

            updated = re.sub(self.css_url_pattern, replace_url, content)

            if content != updated:
                file_path.write_text(updated, encoding="utf-8")
                LOGGER.info("webcontext: updated CSS file: %s", file_path)

        except Exception as e:
            LOGGER.error("webcontext: failed to process %s: %s", file_path, e)


    def on_post_build(self, config):
        context = self.config['context']
        site_dir = Path(config['site_dir'])

        for css_file in site_dir.rglob("*.css"):
            self._process_css_file(css_file, context)
