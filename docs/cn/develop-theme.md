# 制作主题

这篇文档将介绍如何给 [vanellope](https://github.com/qar/vanellope) 制作主题。

# 文档目录

# <a id="toc-files-and-directories"></a>目录结构和文件

一个主题需要包含特定名称的模板文件，并放到名为 `templates` 的目录下，vanellope 将以 `templates` 目录为模板根目录查找文件。我们这里说的模板文件，指的是 [tornado web templates](https://www.tornadoweb.org/en/stable/template.html)。模板中可以使用有限的变量和 Python 语法。模板经过模板引擎渲染后得到 HTML 字符串。

一个主题中 **至少** 需要包含下面目录结构树中提到的模板文件。

```
.
└── templates
    ├── 404.html
    ├── archive.html
    ├── archives.html
    ├── article.html
    ├── category.html
    ├── categories.html
    ├── index.html
    ├── notes.html
    ├── tag.html
    ├── tags.html
    └── welcome.html
```

# <a id="toc-urls-and-templates"></a>模板与路由

一般情况下，一个 URL 对应一个模板文件, 路由与模板以及模板的功能的描述如下:


| URL              | Template        | 说明                                              |
| ---              | ---             | ---                                               |
| \/               | index.html      | 首页                                              |
| \/welcome        | welcome.html    | 激活页面，只有 vanellope 初次安装时会看到这个页面 |
| \/tags           | tags.html       | 标签列表页面                                      |
| \/archives       | archives.html   | 归档列表页面                                      |
| \/categories     | categories.html | 分类列表页面                                      |
| \/notes          | notes.html      | Notes 页面，功能类似 twitter 的时间线             |
| \/tags\/example  | tag.html        | 包含某已标签的文章列表页面                        |
| \/archive/2019   | archive.html    | 具体一个时间段内的文章归档页面                    |
| \/categories/cat | category.html   | 某一分类下文章列表页面                            |

# <a id="toc-template-variables"></a>模板变量

模板内有一些是全局变量，在所有模板间都可以使用（同一个变量名在不同的模板下可能会有不同的值）, 还有一些是模板相关变量，只出现在一个或几个模板内。关于模板变量的更多信息请参考：[模板变量](./template-variables.md)


# <a id="toc-hands-on"></a>动手制作

1. 通过 Docker 在本地启动一个 vanellope 实例:

```
docker pull qiaoanran/vanellope:latest
docker run --rm -v $(pwd)/vanellope_content:/vanellope_content -p 8080:80 --name vanellope-demo qiaoanran/vanellope:v0.3.0-rc
```

运行上述命令后，一个 vanellope 就跑起来了，可以通过 http://localhost:8088 来访问。如果命令中用到的 vanellope\_content 目录不存在的话会被自动创建。vanellope 的数据库等文件都将存在在这个目录下，包括自定义的主题。


2. 最简单的 `hello, world` 模板

```
echo 'hello, world' > ./vanellope_content/themes/my-first-theme/templates/index.html
```

运行上述命令后，打开 http://localhost:8088/controlpanel/#/settings 页面，这个页面下有个 `主题` 选项，可以发现选项中多了一个 `my-first-theme` 的选项, 选择该选项后保存再打开 http://localhost:8088/ 会发现，首页显示的是刚才写入模板的 `hello, world`。虽然简单到只有一个模板文件和几个字符，但这就是一个完全正常可以工作的主题了。配合模板变量就可以展示动态内容了。

