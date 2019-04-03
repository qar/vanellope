# Develop Theme

## Files and Directories
A theme contains some html templates and optional static files like css, javascript .etc.

Different pages require different therefore you need to provide several html templates.

A theme must have this file directory structure.

```
.
└── templates
    ├── 404.html
    ├── archives.html
    ├── article.html
    ├── categories.html
    ├── index.html
    ├── notes.html
    ├── tags.html
    └── welcome.html
```

Files listed above must exist in a theme package. `vanellope` will look for template files in `templates` directory.

## URL and Templates

Tornado will compile template into html. Read [tornado template documentation](https://www.tornadoweb.org/en/stable/template.html) to learn how to write a template.

Different template is used for different page and hint different urls.

| URL              | Template        | Note                                                                             |
| ---              | ---             | ---                                                                              |
| \/               | index.html      | index page, the first page visitors will see                                     |
| \/welcome        | welcome.html    | activation page, only system admin will see this page                            |
| \/tags           | tags.html       | article tags list page but you can use this page for different purpose           |
| \/archives       | archives.html   | articles archive page, but you can use this page for different purpose           |
| \/categories     | categories.html | article categories page, but you can use this page for different purpose         |
| \/notes          | notes.html      | kind of like twitter's timeline, but you can use this page for different purpose |
| \/tags\/example  | tag.html        | articles that have `example` tag                                                 |
| \/archive/2019   | archive.html    | articles publish in 2019                                                         |
| \/categories/cat | category.html   | articles with category `cat`                                                     |

## Template Variables

There is a preinstalled educational theme named `example`, you can use this theme to see what variable is available in a page.

## Global Variables

global variables exist in all template context.

## Tempalte Specific Variables

template specific variables only exist in specific template.

## Get your hands dirty

1. run vanellope on your machine. this can be done by:

```
docker pull qiaoanran/vanellope:latest
docker run --rm -v $(pwd)/vanellope_content:/vanellope_content -p 8080:80 --name vanellope-demo qiaoanran/vanellope:v0.3.0-rc
```

after running those command, a vanellope instance will be running on http://localhost:8088. A direcotry named vanellope\_content will be created if not exist. vanellope will use this directory to store data, and our theme making journary begin with this directory.


2. a `hello, world` template
```
echo 'hello, world' > ./vanellope_content/themes/my-first-theme/templates/index.html
```

now open http://localhost:8088/controlpanel/#/settings page, a `my-first-theme` option will be available, this is your first theme, select this option and click the save button, then visit http://localhost:8088/ (refresh may be required), the page will show `hello, world`

