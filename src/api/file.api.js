import axios from 'axios';
import Files from '../vs-entities/files';

export default {
  getImportableFiles: (storageId, first, number) => {
    const params = {
      matrix: {
        first,
        number,
      },
    };

    return axios.get(`/api/storage/${storageId}/importable`, { params })
      .then((response) => {
        const data = {
          files: [],
          hits: response.data.hits,
        };

        if (response.data.element !== undefined) {
          data.files = new Files(response.data.element);
        }

        return data;
      });
  },
};
