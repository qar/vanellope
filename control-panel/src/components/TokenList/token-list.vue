<template>
  <div>
    <div class="article-list-layout">
      <h1 class="table-title">Access Tokens</h1>
      <Table :columns="columns" :data="rows"></Table>
      <Row>
          <Col span="12">
            <div style="padding-top: 10px; text-align: left">
              <Button type="primary" @click="addToken">Add New Token</Button>
            </div>
          </Col>
          <Col span="12">
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
          </Col>
      </Row>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import apis from '@/utils/api';

export default {
  name: 'TokenList',

  data () {
    return {
      columns: [
        {
          title: 'Token',
          key: 'token',
          className: 'token-item',
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
                    this.remove(params.row.token)
                  }
                }
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
    addToken() {
      apis.addToken()
        .then(res => {
          this.$Notice.open({
            title: '添加成功',
            desc: '',
          });
        })
        .finally(() => {
          this.getTokens(this.paging);
        });
    },

    remove(token) {
      apis.removeToken(token)
        .then(res => {
          this.$Notice.open({
            title: '已移除',
            desc: '',
          });
        })
        .finally(() => {
          this.getTokens(this.paging);
        });
    },

    // 跳转到第 n 页
    changePage(n) {
      this.paging.current = n;
      this.getTokens(this.paging);
    },

    changePageSize(size) {
      this.paging.size = size;
      this.getTokens(this.paging);
    },

    getTokens(paging) {
      if (!paging) {
        paging = {
          size: 20,
          current: 1,
        };
      }
      apis.getTokens(paging)
        .then(res => {
          this.paging.total = res.paging.total;
          this.paging.size = res.paging.items_per_page;

          this.rows = res.data;
        });
    },
  },

  mounted() {
    this.getTokens(this.paging);
  },
};
</script>
<style lang="scss">
  .token-item {
    font-family: Consolas,Menlo,Courier,monospace;
  }
</style>
