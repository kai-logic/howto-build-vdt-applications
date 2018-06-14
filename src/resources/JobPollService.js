import axios from 'axios';

export default class JobPollService {
  constructor({
    jobId, milliseconds = 2000, asset, jobStatusUrl = '/api/job/',
    progressCallback, successCallback, failedCallback,
  }) {
    this.jobId = jobId;
    this.milliseconds = milliseconds;
    this.asset = asset;
    this.jobStatusUrl = jobStatusUrl;
    this.progressCallback = progressCallback;
    this.successCallback = successCallback;
    this.failedCallback = failedCallback;
    this.interval = null;
  }

  startInterval() {
    this.interval = setInterval(() => {
      axios.get(`${this.jobStatusUrl}${this.jobId}`)
        .then((jobUpdate) => {
          if (JobPollService.isValidFunction(this.progressCallback)) {
            this.progressCallback(jobUpdate.data, this.asset);
          }
          if (jobUpdate.data.status === 'FINISHED' || jobUpdate.data.status === 'FINISHED_WARNING') {
            if (JobPollService.isValidFunction(this.successCallback)) {
              this.successCallback(jobUpdate.data, this.asset);
            }
            this.stopInterval();
          } else if (jobUpdate.data.status === 'FAILED_TOTAL' || jobUpdate.data.status === 'ABORTED') {
            if (JobPollService.isValidFunction(this.failedCallback)) {
              this.failedCallback(jobUpdate.data, this.asset);
            }
            this.stopInterval();
          }
        });
    }, this.milliseconds);
  }

  static isValidFunction(cbFunction) {
    return cbFunction !== undefined && cbFunction !== null && typeof cbFunction === 'function';
  }

  stopInterval() {
    clearInterval(this.interval);
  }
}
