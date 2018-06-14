import Item from './item';
import SearchItem from './searchItem';
import Shape from './shape';
// import Timespan from '../vs-entities/timespan';

export default class DetailedItem extends SearchItem {
  constructor(searchItem, item) {
    if (searchItem instanceof SearchItem) {
      super(searchItem);
    } else {
      super(item);
    }
    const flatTimespan = Item.getTimespan(item.metadata, '-INF', '+INF');
    const keyList = {
      originalVideoCodec: 'videoCodec',
      durationSeconds: 'duration',
      originalAudioCodec: 'audioCodec',
      originalFilename: 'filename',
    };

    const metadata = Object.assign(this.metadata, Item.getFields(flatTimespan, keyList));
    this.metadata = metadata;

    this.shapes = Shape.getAllShapes(item.shape);
    this.files = item.files.uri;
    this.timespans = Item.getAllTimespans(item.metadata, '-INF', '+INF');
  }
}
