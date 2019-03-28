/* eslint-disable */
import apis from '@/utils/api';

export default {
  name: 'NoteList',

  data () {
    return {
      // 标题 创建时间 阅读数 评论数
      columns: [
        {
          title: '内容',
          key: 'content',
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
            ]);
          }
        },
      ],

      rows: [],

      content: '',

      modals: {
        compose: false,
      },

      // 分页
      paging: {
        total: 43,
        size: 20, // n * 10
        current: 1,
      },
    };
  },

  methods: {
    addNote() {
      apis.addNote(this.content)
        .then(res => {
          this.content = '';
          this.$Notice.open({
            title: '已添加',
            desc: '',
          });
        })
        .finally(() => {
          this.getArticles(this.paging);
        });
    },

    remove(article) {
      apis.deleteNote(article.uuid)
        .then(res => {
          this.$Notice.open({
            title: '已删除',
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
      apis.getNotes(paging)
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
