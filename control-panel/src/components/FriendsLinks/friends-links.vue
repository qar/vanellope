<template>
  <div>
    <div class="article-list-layout">
      <h1 class="table-title">友链</h1>
      <Table :columns="columns" :data="rows"></Table>

      <Button type="primary" class="add-site" @click="modal1=true">添加站点</Button>

      <Modal
          v-model="modal1"
          title="添加站点"
          @on-ok="ok"
          @on-cancel="cancel">
          <Input v-model="site.title" placeholder="站点标题" />
          <br />
          <Input v-model="site.address" placeholder="站点地址" />
          <br />
          <Input v-model="site.notes" placeholder="备注" />
      </Modal>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import apis from '@/utils/api';

export default {
  name: 'FriendsLinks',

  data() {
    return {
      // 标题 创建时间 阅读数 评论数
      columns: [
        {
          title: '站点名称',
          key: 'title',
          render: (h, params) => {
            return h('div', [
                h('router-link', {
                  props: {
                    to: { name: 'ArticleMarkdownEditor', params: { articleId: params.row.uuid }},
                  },
                }, [
                  h('strong', params.row.title),
                ]),
            ]);
          }
        },

        {
          title: '地址',
          key: 'address',
        },

        {
          title: '备注',
          key: 'notes',
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
                    this.remove(params.row);
                  },
                },
              }),

              h('Button', {
                props: {
                  icon: 'eye',
                  type: 'ghost',
                  size: 'small',
                },
                on: {
                  click: () => {
                    this.preview(params.row);
                  },
                },
              }),
            ]);
          },
        },
      ],

      rows: [],

      site: {
        title: '',
        address: '',
        notes: '',
      },

      modal1: false,
    };
  },

  mounted() {
  },

  methods: {
    save() {},

    ok () {
        this.$Message.info('Clicked ok');
    },
    cancel () {
        this.$Message.info('Clicked cancel');
    }
  },
};
</script>

<style lang="scss">
.article-list-layout {
  .table-title {
    margin-bottom: 1em;
  }

  padding: 40px;

  .paging {
    padding-top: 10px;
    text-align: right;
  }

  .add-site {
    margin-top: 20px;
  }
}
</style>
