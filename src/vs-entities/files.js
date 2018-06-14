export default class Files {
  constructor(files) {
    this.files = [];
    for (let i = 0; i < files.length; i += 1) {
      const searchKeys = Object.keys(files[i].file);
      const fileData = {};
      for (let j = 0; j < searchKeys.length; j += 1) {
        fileData[searchKeys[j]] = files[i].file[searchKeys[j]];
      }
      this.files.push(fileData);
    }
  }
}
