import Vue from 'vue';
import Router from 'vue-router';
import MarkdownEditor from '@/components/MarkdownEditor/markdown-editor.vue';
import ArticleList from '@/components/ArticleList/article-list.vue';
import DraftsList from '@/components/DraftsList/drafts-list.vue';
import Settings from '@/components/Settings/settings.vue';
import TrashCan from '@/components/TrashCan/trash-can.vue';
import WidgetsPage from '@/components/WidgetsPage/widgets-page';
import FriendsLinks from '@/components/FriendsLinks/friends-links';
import CommentList from '@/components/CommentList/comment-list.vue';
import TokenList from '@/components/TokenList/token-list';

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
      component: TrashCan,
    },

    {
      path: '/drafts',
      name: 'DraftsList',
      component: DraftsList,
    },

    {
      path: '/widgets',
      name: 'WidgetsPage',
      component: WidgetsPage,
    },

    {
      path: '/firends-links',
      name: 'FriendsLinks',
      component: FriendsLinks,
    },

    {
      path: '/comments',
      name: 'CommentList',
      component: CommentList,
    },

    {
      path: '/tokens',
      name: 'TokenList',
      component: TokenList,
    },
  ],
});
