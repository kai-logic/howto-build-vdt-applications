// Mapping of timespan
import Timespan from './timespan';

export default class MetadataEvent extends Timespan {
  /**
   * @param {*} timespan - one timespan with one or multiple fields in group or not
   */
  constructor(timespan, name) {
    // If we're buildning on an existing object or not
    super(timespan.orignalTimespan || timespan);
    this.name = name;
    this.field = this.field.filter(field => field.name === this.name);
    // There can only be one field or group with the same name on each timespan
    this.field = this.field[0] || null;
    this.group = this.group[this.name] || null;
  }
}
