import Vue from 'vue';
import Router from 'vue-router';
import HelloWorld from '@/components/HelloWorld';
import MarkdownEditor from '@/components/MarkdownEditor/markdown-editor.vue';
import ArticleList from '@/components/ArticleList/article-list.vue';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld,
    },

    {
      path: '/editor',
      name: 'MarkdownEditor',
      component: MarkdownEditor,
    },

    {
      path: '/articles',
      name: 'ArticleList',
      component: ArticleList,
    },
  ],
});
