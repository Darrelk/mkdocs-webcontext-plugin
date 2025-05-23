# Webcontext link converter plugin for MkDocs

MkDocs assumes absolute paths start from the root of the hosted website, like `http://localhost/`. For example, an absolute path like `/assets/image1.jpg` becomes `http://localhost/assets/image1.jpg`, which is correct if MkDocs is hosted at the root.

When the server root is not the same as the MkDocs root, this plugin lets you define a `webcontext` to prepend to these absolute paths. The `webcontext` path (e.g., `/projectname/documents`) replaces the default root (`/`).

## Features

* Converts absolute image paths in Markdown to be relative to a specified web context.
* Converts image `src` attributes in HTML embedded in Markdown.
* Converts `url("/path")` references inside CSS files.
* Supports Markdown reference-style image and link syntax.
* Debug and info logging of replacements.

### Examples

| Site URL                                                 | Context  | Image Path Before | Image Path After         |
| -------------------------------------------------------- | -------- | ----------------- | ------------------------ |
| [http://example.com/](http://example.com/)               | /        | /images/img1.jpg  | /images/img1.jpg         |
| [http://example.com/foo](http://example.com/foo)         | /foo     | /images/img1.jpg  | /foo/images/img1.jpg     |
| [http://example.com/foo/bar](http://example.com/foo/bar) | /foo/bar | /images/img1.jpg  | /foo/bar/images/img1.jpg |
| [http://127.0.0.1:8000](http://127.0.0.1:8000)           | /        | /images/img1.jpg  | /images/img1.jpg         |
| [http://127.0.0.1:8000/foo](http://127.0.0.1:8000/foo)   | /foo     | /images/img1.jpg  | /foo/images/img1.jpg     |

## Quick Start

1. Install the plugin:

   ```bash
   pip install mkdocs-webcontext-plugin
   ```

   Or using Poetry:

   ```bash
   poetry add mkdocs-webcontext-plugin
   ```

2. Enable the plugin in your `mkdocs.yml`:

   ```yaml
   plugins:
     - webcontext:
         context: foo/bar
   ```

## Supported Link Types

The plugin modifies the following path formats:

* Markdown links: `[title](/path/image.png)`
* Markdown reference links:

  ```markdown
  [logo]: /assets/logo.png
  ```
* HTML image tags: `<img src="/assets/img.png">`
* CSS `url()` paths: `url("/assets/bg.jpg")`

These paths will be rewritten to start with your defined `context`.

## CSS Support

After your site is built, the plugin will scan all `.css` files in the output directory and rewrite any `url("/...")` references to use the defined `context`.

## Logging

Rewrites are logged at the `DEBUG` level. Updated CSS files are logged at the `INFO` level.

## Special Thanks

This plugin was inspired by and built with guidance from:

* [byrnereese/mkdocs-plugin-template](https://github.com/byrnereese/mkdocs-plugin-template)
* [sander76/mkdocs-abs-rel-plugin](https://github.com/sander76/mkdocs-abs-rel-plugin)
