// import Shape from './shape';

export default class Item {
  static getTimespan(metadata, start, end) {
    let i = 0;
    for (i; i < metadata.timespan.length; i += 1) {
      if (metadata.timespan[i].start === start && metadata.timespan[i].end === end) {
        break;
      }
    }
    return metadata.timespan[i];
  }

  static getAllTimespans(metadata, excludeStart, excludeEnd) {
    let timespans = [];
    if (excludeStart || excludeEnd) {
      for (let i = 0; i < metadata.timespan.length; i += 1) {
        if (metadata.timespan[i].start !== excludeStart &&
            metadata.timespan[i].end !== excludeEnd) {
          timespans.push(metadata.timespan[i]);
        }
      }
    } else {
      ({ timespans } = metadata);
    }

    return timespans;
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
