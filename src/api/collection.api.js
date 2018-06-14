import axios from 'axios';
import SearchCollection from '../vs-entities/searchCollection';

export default {
  getCollections: (query, first, number) => {
    const data = {
      query,
      first,
      number,
      content: 'metadata',
      field: 'collectionId,title,created,user',
    };

    return axios.put('/api/collections', data)
      .then(response => [{
        collections: response.data.collection !== undefined
          ? response.data.collection.map(collection => new SearchCollection(collection)) : [],
        hits: response.data.hits,
      }][0]);
  },
};
