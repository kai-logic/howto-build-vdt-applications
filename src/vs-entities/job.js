export default class Job {
  static getKeys(job, keyList) {
    const metadata = {};
    Object.keys(job).forEach((key) => {
      if (keyList[key]) {
        metadata[keyList[key]] = job[key];
      }
    });
    return metadata;
  }

  /*
  static getMetadataKeys(job, keyList) {
    const metadata = {};
    for (let i = 0; i < keyList.length; i += 1) {
      metadata.push(keyList[i]);
    }
    return metadata;
  }
  */
}
