/* eslint-disable */
import $http from '@/utils/http';

function getNotes(paging) {
  const params = {
    p: paging.current,
    z: paging.size,
  };
  return $http.get('/api/v1/notes', { params })
    .then(res => res.data);
}

function deleteNote(id) {
  return $http.delete(`/api/v1/notes/${id}`)
    .then(res => res.data);
}

function addNote(content) {
  return $http.post('/api/v1/notes', { content })
    .then(res => res.data);
}

function getTokens(paging) {
  const params = {
    p: paging.current,
    z: paging.size,
  };
  return $http.get('/api/v1/access-tokens', { params })
    .then(res => res.data);
}

function addToken() {
  return $http.post(`/api/v1/access-tokens`)
    .then(res => res.data);
}

function removeToken(token) {
  return $http.delete(`/api/v1/access-tokens/${token}`)
    .then(res => res.data);
}

function getUserProfile() {
  return $http.get('/api/v1/profile').then(res => res.data);
}

function updateUserProfile(profile) {
  return $http.put('/api/v1/profile', profile).then(res => res.data);
}

function getSettings() {
  return $http.get('/api/v1/configuration').then(res => res.data);
}

function updateSettings(settings) {
  return $http.put('/api/v1/configuration', settings).then(res => res.data);
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
    s: ['published'],
    p: paging.current,
    z: paging.size,
  };
  return $http.get('/api/v1/posts', { params })
    .then(res => res.data);
}

function getCommentList(paging, states=['checking']) {
  const params = {
    s: states,
    p: paging.current,
    z: paging.size,
  };
  return $http.get('/api/v1/comments', { params })
    .then(res => res.data);
}

function updateComment(params) {
  return $http.put('/api/v1/comments', params)
    .then(res => res.data);
}

function getDraftList(paging) {
  const params = {
    s: ['draft'],
    p: paging.current,
    z: paging.size,
  };
  return $http.get('/api/v1/posts', { params })
    .then(res => res.data);
}

function deleteArticle(id) {
  return $http.delete(`/api/v1/posts/${id}`)
    .then(res => res.data);
}

function getTrash(paging) {
  const params = {
    p: paging.current,
    z: paging.size,
  };

  return $http.get('/api/v1/trash', { params }).then(res => res.data);
}

function getArticle(id) {
  return $http.get(`/api/v1/posts/${id}`)
    .then(res => res.data);
}

function getFriendLinks() {
  return $http.get('/api/v1/admin/friend-links').then(res => res.data);
}

function createFriendLinks(site) {
  return $http.post('/api/v1/admin/friend-links', site).then(res => res.data);
}

function delFriendLink(linkId) {
  return $http.delete(`/api/v1/admin/friend-links/${linkId}`).then(res => res.data);
}

function getTags() {
  return $http.get('/api/v1/tags').then(res => res.data);
}

function sendVerifyLinkToEmail(email) {
  return $http.post('/api/v1/verify/email', { email })
}

export default {
  addToken,
  createArticle,
  updateArticle,
  updateSettings,
  getArticleList,
  getCommentList,
  getDraftList,
  getArticle,
  getSettings,
  getTrash,
  getTags,
  getTokens,
  removeToken,
  deleteArticle,
  getFriendLinks,
  getNotes,
  addNote,
  deleteNote,
  createFriendLinks,
  delFriendLink,
  updateComment,
  getUserProfile,
  updateUserProfile,
  sendVerifyLinkToEmail
};
