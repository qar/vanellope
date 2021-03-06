/* eslint-disable */
import apis from '@/utils/api';

export default {
  name: 'ArticleList',

  data () {
    return {
      // 标题 创建时间 阅读数 评论数
      columns: [
        {
          title: '标题',
          key: 'title',
          render: (h, params) => {
            return h('a', {
              attrs: {
                href: `/article/${params.row.uuid}`,
                title: params.row.title,
                target: '_blank',
              },
            }, [
              h('strong', params.row.title),
            ]);
          },
        },

        {
          title: '预览',
          key: 'summary',
          ellipsis: true,
          tooltip: true,
          size: 'large',
          className: 'summary-text',
        },

        {
          title: '分类',
          key: 'category',
          sortable: true,
          render: (h, params) => {
            return h('SPAN', params.row.category || '-');
          },
        },

        {
          title: '标签',
          key: 'tags',
          className: 'tag-list',
          render: (h, params) => {
            const tags = params.row.tags.map(t => h('SPAN', t));
            return h('P', tags);
          },
        },

        {
          title: '创建时间',
          key: 'created_at',
          sortable: true,
          render: (h, params) => {
            const ts = new Date(params.row.created_at * 1000).toLocaleString();
            return h('SPAN', ts);
          },
        },

        {
          title: '阅读数',
          key: 'counts',
        },

        {
          title: '操作',
          key: 'action',
          width: 150,
          align: 'center',
          render: (h, params) => {
            return h('ButtonGroup', [
              h('Button', {
                props: {
                  icon: 'trash-a',
                  type: 'ghost',
                  size: 'small',
                },
                on: {
                  click: () => {
                    this.remove(params.row)
                  }
                }
              }),

              h('Button', {
                props: {
                  icon: 'compose',
                  type: 'ghost',
                  size: 'small',
                  to: { name: 'ArticleMarkdownEditor', params: { articleId: params.row.uuid }}
                },

                on: {
                  click: () => {
                    this.$router.push({
                      name: 'ArticleMarkdownEditor',
                      params: { articleId: params.row.uuid }
                    });
                  },
                },
              }),
            ]);
          }
        },
      ],

      rows: [],

      // 分页
      paging: {
        total: 43,
        size: 20, // n * 10
        current: 1,
      },
    };
  },

  methods: {
    preview(article) {
      window.location.href = `/article/${article.uuid}`;
    },

    remove(article) {
      apis.deleteArticle(article.uuid)
        .then(res => {
          this.$Notice.open({
            title: '文章已移如垃圾箱',
            desc: '',
          });
        })
        .catch(err => {
          console.log('DEBUG delete article', err);
        })
        .finally(() => {
          this.getArticles(this.paging);
        });
    },

    // 跳转到第 n 页
    changePage(n) {
      this.paging.current = n;
      this.getArticles(this.paging);
    },

    changePageSize(size) {
      this.paging.size = size;
      this.getArticles(this.paging);
    },

    getArticles(paging) {
      if (!paging) {
        paging = {
          size: 20,
          current: 1,
        };
      }
      apis.getArticleList(paging)
        .then(res => {
          this.paging.total = res.paging.total;
          this.paging.size = res.paging.items_per_page;
          this.rows = res.data;
        });
    },
  },

  mounted() {
    this.getArticles(this.paging);
  },
};
