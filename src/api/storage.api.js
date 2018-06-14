import axios from 'axios';
import Storage from '../vs-entities/storage';

export default {
  // Storage metadata needs modelling when we start using it
  getStorages: status => axios.get(`/api/storages?status=${status}`)
    .then((response) => {
      const storages = response.data.storage.map(storage => new Storage(storage).data);
      return storages;
    }),
};
