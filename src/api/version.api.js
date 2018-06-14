import axios from 'axios';

export default {
  getVersion: () => axios.get('/api/version')
    .then(response => response),
};
