import Job from './job';

export default class SearchJob extends Job {
  constructor(job) {
    super();
    if (job instanceof SearchJob) {
      const searchKeys = Object.keys(job);
      for (let i = 0; i < searchKeys.length; i += 1) {
        this[searchKeys[i]] = job[searchKeys[i]];
      }
    } else {
      const keyList = {
        jobId: 'id',
        user: 'user',
        started: 'started',
        status: 'status',
        type: 'type',
        priority: 'priority',
      };

      this.metadata = Object.assign({}, Job.getKeys(job, keyList));
    }
  }
}
