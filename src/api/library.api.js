import axios from 'axios';
import SearchLibrary from '../vs-entities/searchLibrary';

export default {
  getLibraries: (updateMode, first, number) => {
    const data = {
      updateMode,
      first,
      number,
    };

    return axios.put('/api/libraries', data)
      .then(response => [{
        libraries: response.data.uri !== undefined
          ? response.data.uri.map(library => new SearchLibrary(library)) : [],
        hits: response.data.hits,
      }][0]);
  },
};
