import sys
from shutil import rmtree
from pathlib import Path
from setuptools import setup, Command

setup(
    name="mkdocs-webcontext-plugin",
    version="0.1.0",
    packages=["mkdocs_webcontext_plugin"],
    url="https://github.com/darrelk/mkdocs-webcontext-plugin",
    license="MIT",
    author="darrelk",
    author_email="darrelkley@gmail.com",
    description="Mkdocs plugin to convert absolute paths to Webcontext aware paths.",
    long_description=README,
    long_description_content_type="text/markdown",
    entry_points={
        "mkdocs.plugins": [
            "webcontext = mkdocs_webcontext_plugin:Webcontext"
        ]
    }
)
