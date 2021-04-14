# Webcontext link converter plugin for mkdocs

MkDocs allows absulute paths assuming that the site is deployed to the root of the hosted website like "http://localhost/". When using the following absolute path "/assets/image1.jpg" it is actually using "http://localhost/assets/image1.jpg" which is correct if the MkDocs is deployed to the site root.

When the server root is not the same as the MkDocs root, the webcontext plugin can be used to define a webcontext to use instead of the defined root. The webcontext path which can be anyting like "/projectname/documents" is used where "/" is defined.

Some examples of site urls before and after using the webcontext plugin:
Site Url | Context  | Image before | Image after 
---------|----------|--------------|------------ 
http://example.com/        | / | /images/img1.jpg | /images/img1.jpg
http://example.com/foo     | /foo | /images/img1.jpg | /foo/images/img1.jpg
http://example.com/foo/bar | /foo/bar | /images/img1.jpg | /foo/bar/images/img1.jpg
http://127.0.0.1:8000      | / | /images/img1.jpg | /images/img1.jpg
http://127.0.0.1:8000/foo  | /foo | /images/img1.jpg | /foo/images/img1.jpg


## Quick start

1. Install the module using pip: `pip install mkdocs-webcontext`

2. In your project, add a plugin configuration to `mkdocs.yml`:

   ```yaml
   plugins:
     - webcontext:
         context: foo/bar
   ```

Special thanks to the following repositories for guidance:

* [byrnereese/mkdocs-plugin-template](https://github.com/byrnereese/mkdocs-plugin-template)
* [sander76/mkdocs-abs-rel-plugin](https://github.com/sander76/mkdocs-abs-rel-plugin)