# 模板变量

# <a id="toc-all-vars"></a>全部模板变量

| Name              | Type    | Scope       | Example                              |
| ---               | ---     | ---         | ---                                  |
| ctx               | dict    | global      | [ctx](#toc-global-ctx)               |
| site              | dict    | global      | [site](#toc-global-site)             |
| title             | unicode | global      |                                      |
| page              | unicode | global      |                                      |
| description       | unicode | global      |                                      |
| req               | dict    | global      |                                      |
| archives          | dict    | global      |                                      |
| tags              | list    | global      |                                      |
| categories        | list    | global      |                                      |
| frientlinks       | list    | global      |                                      |
| current\_page     | int     | index,      |                                      |
| next\_page        | int     | index, tags |                                      |
| previous\_page    | int     | index, tags |                                      |
| pages             | int     | index,      |                                      |
| current\_uri      | unicode | index,      |                                      |
| articles          | list    | index,      | list of [article](#toc-vars-article) |
| drafts            | list    | index,      |                                      |
| notes             | list    | notes,      | list of [note](#toc-vars-note)       |
| article           | dict    | article     | [article](#toc-vars-article)         |
| related\_articles | list    | article,    | list of [article](#toc-vars-article) |
| siblings          | list    | article,    | list of [article](#toc-vars-article) |
| comments          | list    | article,    | list of [comment](#toc-vars-comment) |


# <a id="toc-global-ctx"></a>ctx

| Name | Type |
| ---  | ---  |
| year | int  |

# <a id="toc-global-site"></a>site

| Name                    | Type    | Example             |
| ---                     | ---     | ---                 |
| site\_comment\_enabled  | unicode | no                  |
| site\_tracking\_id      | unicode |                     |
| site\_lang              | unicode | zh-CN               |
| default\_category       | unicode | life                |
| posts\_per\_page        | unicode | 10                  |
| draft\_base\_path       | unicode | /drafts/            |
| google\_adsense         | unicode |                     |
| site\_url               | unicode |                     |
| site\_description       | unicode | Life with vanellope |
| site\_title             | unicode | Life with vanellope |
| site\_theme             | unicode | simple              |
| site\_tracking\_enabled | unicode | yes                 |
| site\_comment\_id       | unicode |                     |
| site\_tracking          | unicode |                     |
| site\_comment           | unicode |                     |

# <a id="toc-global-req"></a>req

| Name        | Type    | Example |
| ---         | ---     | ---     |
| path        | unicode |         |
| hostname    | unicode |         |
| user\_agent | unicode |         |

# <a id="toc-vars-article"></a> article

| Name        | Type              | Example                        |
| ---         | ---               | ---                            |
| category    | unicode           | 333333333                      |
| editor-path | unicode           | /controlpanel#/editor/7cb6c56e |
| uuid        | unicode           | 7cb6c56e                       |
| title       | unicode           | ddd                            |
| updated\_at | datetime.datetime | 2019-04-03 04:50:28.193673     |
| created\_at | datetime.datetime | 2019-04-03 04:29:12.321093     |
| tags        | list              | [u'tag1', u'dddd']             |
| state       | unicode           | published                      |
| summary     | unicode           | dddd                           |
| content     | unicode           | <p>dddd</p>                    |
| source      | unicode           | dddd                           |
| ext         | unicode           | markdown                       |
| path        | unicode           | /article/7cb6c56e+ddd          |
| counts      | int               | 140                            |


# <a id="toc-vars-note"></a>note

| Name        | Type              | Example                    |
| ---         | ---               | ---                        |
| content     | unicode           | dddd                       |
| created\_at | datetime.datetime | 2019-04-03 10:48:59.020786 |
| uuid        | unicode           | 9a545135                   |
| updated\_at | datetime.datetime | 2019-04-03 10:48:59.020800 |

# <a id="toc-vars-comment"></a>comment

| Name        | Type              | Example                    |
| ---         | ---               | ---                        |
| uuid        | unicode           | cf7fd5cb                   |
| post\_title | unicode           | ddd                        |
| created\_at | datetime.datetime | 2019-04-05 11:23:04.260514 |
| content     | unicode           | asdfasdfasd                |
| post\_id    | unicode           | 7cb6c56e                   |
| state       | unicode           | approved                   |
| email       | unicode           |                            |
| name        | unicode           | dddd                       |


