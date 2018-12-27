/* eslint-disable */
import apis from '@/utils/api';

export default {
  name: 'CommentList',

  data () {
    return {
      activeState: 'checking',

      // 标题 创建时间 阅读数 评论数
      columns: [
        {
          title: '评论内容',
          key: 'content',
        },

        {
          title: '用户名',
          key: 'name',
        },

        {
          title: '邮箱',
          key: 'email',
        },

        {
          title: '文章',
          key: 'post_title',
        },

        {
          title: '提交时间',
          key: 'created_at',
          render: (h, params) => {
            return h('SPAN', [
              new Date(parseInt(params.row.created_at, 10) * 1000).toLocaleString()
            ]);
          },
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
                  icon: 'heart',
                  type: 'ghost',
                  size: 'small',
                },
                on: {
                  click: () => {
                    this.approve(params.row.uuid)
                  }
                }
              }),

              h('Button', {
                props: {
                  icon: 'heart-broken',
                  type: 'ghost',
                  size: 'small',
                },

                on: {
                  click: () => {
                    this.disapprove(params.row.uuid)
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
    approve(uuid) {
      apis.updateComment({ uuid, state: 'approved' })
        .then(res => {
          this.$Notice.open({
            title: '该评论已被允许显示',
            desc: '',
          });
        })
        .catch(err => {
          console.log('DEBUG update comment', err);
        })
        .finally(() => {
          this.getComments(this.paging);
        });
    },

    disapprove(uuid) {
      apis.updateComment({ uuid, state: 'banned' })
        .then(res => {
          this.$Notice.open({
            title: '该评论已被禁止显示',
            desc: '',
          });
        })
        .catch(err => {
          console.log('DEBUG update comment', err);
        })
        .finally(() => {
          this.getComments(this.paging);
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

    getComments(paging, states=['checking']) {
      if (!paging) {
        paging = {
          size: 20,
          current: 1,
        };
      }
      apis.getCommentList(paging, states)
        .then(res => {
          this.paging.total = res.paging.total;
          this.paging.size = res.paging.items_per_page;
          this.rows = res.data;
        });
    },
  },

  mounted() {
    this.getComments(this.paging);
  },
};
