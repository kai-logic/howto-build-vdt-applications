import Item from './item';

export default class SearchItem extends Item {
  constructor(item) {
    super();
    if (item instanceof SearchItem) {
      const searchKeys = Object.keys(item);
      for (let i = 0; i < searchKeys.length; i += 1) {
        this[searchKeys[i]] = item[searchKeys[i]];
      }
    } else {
      const flatTimespan = Item.getTimespan(item.metadata, '-INF', '+INF');
      const keyList = {
        itemId: 'id',
        title: 'title',
        created: 'created',
        originalFormat: 'originalFormat',
        originalFilename: 'filename',
        mediaType: 'mediaType',
        user: 'user',
        representativeThumbnailNoAuth: 'representativeThumbnail',
      };

      this.metadata = Object.assign({}, Item.getFields(flatTimespan, keyList));
      // this.thumbnail = this.metadata.representativeThumbnail;

      // format APInoatuh -> apinoauth
      if (this.metadata.representativeThumbnail) {
        const end = this.metadata.representativeThumbnail
          .slice(11, this.metadata.representativeThumbnail.length);
        this.thumbnail = `/apinoauth/${end}`;
      } else {
        this.thumbnail = '';
      }
    }
  }
}
