/* eslint-disable */
import apis from '@/utils/api';

export default {
  name: 'ArticleList',

  data () {
    return {
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
      ],

      rows: [],
    };
  },

  mounted() {
    apis.getArticleList().then(res => {
      console.log(res);
      this.rows = res.data.map(article => {
        return {
          title: article.title,
          uuid: article.uuid,
        };
      });
    });
  },
};
