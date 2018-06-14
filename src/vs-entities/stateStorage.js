import Storage from './storage';

export default class StateStorage extends Storage {
  constructor(storage) {
    super();
    if (storage instanceof StateStorage) {
      const searchKeys = Object.keys(storage);
      for (let i = 0; i < searchKeys.length; i += 1) {
        this[searchKeys[i]] = storage[searchKeys[i]];
      }
    } else {
      /*
      const searchKeys = Object.keys(storage);
      for (let i = 0; i < searchKeys.length; i += 1) {
        this[searchKeys[i]] = storage[searchKeys[i]];
      }

      const keyList = {
        id: 'id',
        freeCapacity: 'freeCapacity',
        showImportables: 'showImportables',
        state: 'state',
        type: 'type',
      };

      this.metadata = Storage.getKeys(storage, keyList);
      this.method = storage.method;
      */
    }
  }
}
