import axios from 'axios';

export default {
  getShapeTags: () => axios.get('/api/shape-tag')
    .then((response) => {
      const tags = response.data.uri;
      return tags;
    }),
};
