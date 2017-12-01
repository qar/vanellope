/* eslint-disable */
import $http from '@/utils/http';

function createArticle() {}

function getArticleList() {
  return $http.get('/api/v1/posts')
    .then(res => res.data);
}

export default {
  createArticle,
  getArticleList,
};
