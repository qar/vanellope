/* eslint-disable */
import $http from '@/utils/http';

function getSettings() {
  return $http.get('/api/v1/configuration').then(res => res.data);
}

function createArticle(args) {
  return $http.post('/api/v1/posts', args)
    .then(res => res.data);
}

function getArticleList() {
  return $http.get('/api/v1/posts?s=draft&s=published')
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
  getSettings,
};
