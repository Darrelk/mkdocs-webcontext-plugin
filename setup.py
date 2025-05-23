import sys
from shutil import rmtree
from pathlib import Path
from setuptools import setup, Command

HERE = Path(__file__).parent
README = (HERE.joinpath("readme.md")).read_text()

setup(
    name="mkdocs-webcontext-plugin",
    version="0.1.1",
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
