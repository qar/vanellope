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
            return h('div', [
                h('router-link', {
                  props: {
                    to: { name: 'ArticleMarkdownEditor', params: { articleId: params.row.uuid }}
                  },
                }, [
                  h('strong', params.row.title)
                ]),
            ]);
          }
        },

        {
          title: '评论数',
          key: 'comments',
        },

        {
          title: '阅读数',
          key: 'views',
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

          this.rows = res.data.map(article => {
            return {
              title: article.title,
              uuid: article.uuid,
            };
          });
        });
    },
  },

  mounted() {
    this.getArticles(this.paging);
  },
};
