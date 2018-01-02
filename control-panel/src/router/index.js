import Vue from 'vue';
import Router from 'vue-router';
import MarkdownEditor from '@/components/MarkdownEditor/markdown-editor.vue';
import ArticleList from '@/components/ArticleList/article-list.vue';
import Settings from '@/components/Settings/settings.vue';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'ArticleList',
      component: ArticleList,
    },

    {
      path: '/editor',
      name: 'MarkdownEditor',
      component: MarkdownEditor,
    },

    {
      path: '/editor/:articleId',
      name: 'ArticleMarkdownEditor',
      component: MarkdownEditor,
    },

    {
      path: '/settings',
      name: 'Settings',
      component: Settings,
    },

    {
      path: '/trash',
      name: 'Trash',
      component: Settings,
    },

    {
      path: '/draft',
      name: 'Draft',
      component: Settings,
    },
  ],
});
