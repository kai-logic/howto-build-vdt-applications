import Library from './library';

export default class SearchLibrary extends Library {
  constructor(library) {
    super();
    if (library instanceof SearchLibrary) {
      const searchKeys = Object.keys(library);
      for (let i = 0; i < searchKeys.length; i += 1) {
        this[searchKeys[i]] = library[searchKeys[i]];
      }
    } else {
      this.metadata = {
        id: library,
      };
    }
  }
}
