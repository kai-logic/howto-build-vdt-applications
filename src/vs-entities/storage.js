export default class Storage {
  constructor(storage) {
    this.data = storage;
    const [host] = this.data.method[0].uri.split(':');
    const [name] = this.data.method[0].uri.split('@').slice(-1);

    if (host.indexOf('s3') > -1) {
      this.data.name = `${host}://${name.split('?')[0]}`;
    } else {
      this.data.name = name;
    }
  }

  static getKeys(storage, keyList) {
    const metadata = {};
    for (let i = 0; i < keyList.length; i += 1) {
      metadata.push(keyList[i]);
    }
    return metadata;
  }
}
