export default class Timespan {
  /**
     * @param {*} timespan - one timespan with one or multiple fields in group or not
     */
  constructor(timespan) {
    this.originalTimespan = timespan;
    this.start = Timespan.formatTimeCodesToSec(timespan.start);
    this.end = Timespan.formatTimeCodesToSec(timespan.end);
    // this.fieldValues();
    this.field = this.fieldValues();
    this.group = this.groupValues();
  }

  fieldValues() {
    return this.originalTimespan.field.map(field => Timespan.formatField(field));
  }

  groupValues() {
    // Reduce all the groups fields into one array with formattedFields
    return this.originalTimespan.group.reduce((allFields, group) => {
      const abc = allFields;
      const formattedFields = group.field.map(field => Timespan.formatField(field));
      abc[group.name] = formattedFields;
      return abc;
    }, {});
  }

  static formatField(field) {
    const eventField = {};
    Object.keys(field).forEach((key) => {
      if (key === 'value') {
        eventField[key] = field[key][0].value;
      } else {
        eventField[key] = field[key];
      }
    });
    return eventField;
  }

  /**
   * Get all timespans from an Array that matches a name
   * @param {Array} timespans - Timespans to filter
   * @param {String} name - the timespan field or group name to get
   * @returns {Array} filteredTimespans - only timespans with field or group matching @param name
   */
  static getTimespansByName(timespans, name) {
    const filteredTimespans = timespans.filter((timespan) => {
      // Check all fields for matching name
      for (let i = 0; i < timespan.field.length; i++) {
        if (timespan.field[i].name === name) {
          return true;
        }
      }

      // Check all groups for matching name
      for (let i = 0; i < timespan.group.length; i++) {
        if (timespan.group[i].name === name) {
          return true;
        }
      }

      return false;
    });

    return filteredTimespans;
  }
  /**
   * Return any valid timecode (http://apidoc.vidispine.com/latest/time.html#time-codes) to seconds
   * @param {Number, String} time - 124, 124222@44100, 400@30000:1001, 400@NTSC
   */
  static formatTimeCodesToSec(timeCode) {
    // Check if string sample@denominator or sample@denominator:numerator
    // http://apidoc.vidispine.com/latest/time.html
    if (timeCode.indexOf('@') > -1) {
      const timeCodeArray = timeCode.split('@'); // ["sample", "denominator{:numerator}"]
      if (timeCodeArray.length > 2) {
        throw Error('Invalid time representation');
      }

      // Set the time sample
      const sample = parseFloat(timeCodeArray[0], 10);
      const denominatorTimeBase = timeCodeArray[1];
      let timeBase = null;

      // Format the time base
      switch (denominatorTimeBase) {
        case 'PAL':
          timeBase = 25;
          break;
        case 'NTSC':
          timeBase = 30000 / 1001;
          break;
        case 'NTSC30':
          timeBase = 30;
          break;
        default:
          // if denominator:numerator
          if (denominatorTimeBase.indexOf(':') > -1) {
            const timebaseArray = denominatorTimeBase.split(':');
            const denominator = parseInt(timebaseArray[0], 10);
            const numerator = parseInt(timebaseArray[1], 10);
            timeBase = denominator / numerator;
          } else { // if only denominator
            timeBase = parseInt(denominatorTimeBase, 10);
          }
          break;
      }

      return sample / timeBase;
    }

    return parseFloat(timeCode);
  }

  /**
   * @param {Array} timespans - Timespans to fetch names from
   * @returns { Array } names - All names of fields and groups. Does not inluce group-field names.
   */
  static allRootNames(timespans) {
    const names = [];

    function isInArray(name) {
      return names.indexOf(name) > -1;
    }

    timespans.forEach((timespan) => {
      timespan.field.forEach((field) => {
        if (!isInArray(field.name)) {
          names.push(field.name);
        }
      });

      timespan.group.forEach((group) => {
        if (!isInArray(group.name)) {
          names.push(group.name);
        }
      });
    });

    return names;
  }
}
