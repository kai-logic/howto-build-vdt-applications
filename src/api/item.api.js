import axios from 'axios';
import SearchItem from '../vs-entities/searchItem';
import DetailedItem from '../vs-entities/detailedItem';

export default {
  getItems: (query, first, number) => {
    const data = {
      query,
      first,
      number,
      contentPath: '',
      fieldPath: 'itemId,title,created,user,originalFormat,originalFilename,mediaType,representativeThumbnailNoAuth',
    };

    return axios.put('/api/items', data)
      .then(response => ({
        items: response.data.item !== undefined
          ? response.data.item.map(item => new SearchItem(item)) : [],
        hits: response.data.hits,
      }));
  },

  getItem: (itemId, oldItem) => {
    const content = 'metadata,shape,thumbnail,uri';

    return axios.get(`/api/item/${itemId}?content=${content}&methodType=AUTO`)
      .then((response) => {
        const item = response.data !== undefined ? response.data : {};
        return new DetailedItem(oldItem, item);
      });
  },
};
