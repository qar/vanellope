<template>
  <div>
    <Table :columns="columns" :data="rows"></Table>
    <div class="paging">
      <Page
        :total="paging.total"
        :page-size="paging.size"
        show-elevator
        show-sizer
        @on-change="changePage"
        @on-page-size-change="changePageSize">
      </Page>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import apis from '@/utils/api';

export default {
  name: 'CommentsTable',

  props: {
    state: String,
  },

  data() {
    const self = this;

    return {
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
            const children = [];

            if (self.state === 'checking' || self.state === 'approved') {
              children.push(h('Button', {
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
              }));
            }

            if (self.state === 'checking' || self.state === 'banned') {
              children.push(h('Button', {
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
              }));
            }

            return h('ButtonGroup', children);
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
      console.debug('approving comment which id is ', uuid);
      apis.updateComment({ uuid, state: 'approved' })
        .then(res => {
          this.$Notice.open({
            title: '该评论已被允许显示',
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
      console.debug('banding comment which id is ', uuid);
      apis.updateComment({ uuid, state: 'banned' })
        .then(res => {
          this.$Notice.open({
            title: '该评论已被禁止显示',
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

    getComments(paging) {
      if (!paging) {
        paging = {
          size: 20,
          current: 1,
        };
      }
      apis.getCommentList(paging, [this.state])
        .then(res => {
          this.paging.total = res.paging.total;
          this.paging.size = res.paging.items_per_page;
          this.rows = res.data;
        });
    },

    // Exposed to parent component
    update() {
      console.debug('refreshing comment of state', this.state);
      this.getComments();
    },
  },

  mounted() {
    console.debug('Checkout comments which state is', this.state);
    this.getComments(this.paging);
  },
}
</script>

<style lang="scss">
  .paging {
    padding-top: 10px;
    text-align: right;
  }
</style>
