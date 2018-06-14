export default class Collection {
  static getTimespan(metadata, start, end) {
    let i = 0;
    for (i; i < metadata.timespan.length; i += 1) {
      if (metadata.timespan[i].start === start && metadata.timespan[i].end === end) {
        break;
      }
    }
    return metadata.timespan[i];
  }

  static getFields(timespan, keyList) {
    const metadata = {};
    for (let i = 0; i < timespan.field.length; i += 1) {
      if (keyList[timespan.field[i].name]) {
        metadata[keyList[timespan.field[i].name]] = timespan.field[i].value[0].value;
      }
    }
    return metadata;
  }
}
