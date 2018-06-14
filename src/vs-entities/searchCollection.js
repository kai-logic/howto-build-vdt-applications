import Collection from './collection';

export default class SearchCollection extends Collection {
  constructor(collection) {
    super();
    if (collection instanceof SearchCollection) {
      const searchKeys = Object.keys(collection);
      for (let i = 0; i < searchKeys.length; i += 1) {
        this[searchKeys[i]] = collection[searchKeys[i]];
      }
    } else {
      const flatTimespan = Collection.getTimespan(collection.metadata, '-INF', '+INF');
      const keyList = {
        collectionId: 'id',
        title: 'title',
        created: 'created',
        user: 'user',
      };

      this.metadata = Object.assign({}, Collection.getFields(flatTimespan, keyList));
    }
  }
}
