/* eslint-disable */
import $http from '@/utils/http';

function getSettings() {
  return $http.get('/api/v1/configuration').then(res => res.data);
}

function createArticle(args) {
  return $http.post('/api/v1/posts', args)
    .then(res => res.data);
}

function updateArticle(id, args) {
  return $http.put(`/api/v1/posts/${id}`, args)
    .then(res => res.data);
}

function getArticleList(paging) {
  const params = {
    s: ['published', 'draft'],
    p: paging.current,
    z: paging.size,
  };
  return $http.get('/api/v1/posts', { params })
    .then(res => res.data);
}

function getArticle(id) {
  return $http.get(`/api/v1/article/${id}`)
    .then(res => res.data);
}

export default {
  createArticle,
  updateArticle,
  getArticleList,
  getArticle,
  getSettings,
};
