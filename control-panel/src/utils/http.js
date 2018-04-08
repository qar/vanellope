import axios from 'axios';

// Place to add some config
axios.interceptors.response.use(null, (error) => {
  if (error.response.status === 403) {
    window.location = '/login';
  }
  return Promise.reject(error);
});

export default axios;
