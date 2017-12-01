/* eslint-disable */
import $http from '@/utils/http';

function createArticle() {}

function getArticleList() {
  return $http.get('/api/v1/posts')
    .then(res => res.data);
}

function getArticle(id) {
  return $http.get(`/api/v1/article/${id}`)
    .then(res => res.data);
}

export default {
  createArticle,
  getArticleList,
  getArticle,
};
