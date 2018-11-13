<template>
  <div>
    <div class="article-list-layout">
      <h1 class="table-title">友链</h1>
      <Table :columns="columns" :data="rows"></Table>

      <Button type="primary" class="add-site" @click="modal=true">添加站点</Button>
    </div>

    <Modal v-model="modal"
        title="添加站点"
        @on-ok="ok"
        @on-cancel="cancel">
        <Input class="input-box" v-model="site.title" placeholder="站点标题" />
        <Input class="input-box" v-model="site.address" placeholder="站点地址" />
        <Input class="input-box" v-model="site.notes" placeholder="备注" />
    </Modal>
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

      modal: false,
    };
  },

  mounted() {
    this.getLinks();
  },

  methods: {
    getLinks() {
      apis.getFriendLinks().then(res => {
        this.rows = res.data;
      });
    },

    preview(link) {
      open(link.address, '_blank');
    },

    remove(link) {
      apis.delFriendLink(link.uuid)
        .then(() => {
          this.getLinks();
        });
    },

    ok () {
      apis.createFriendLinks(this.site)
        .then(() => {
          this.getLinks();
        });
    },

    cancel () {},
  },
};
</script>

<style lang="scss">
.input-box {
  margin-bottom: 10px;
}

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
