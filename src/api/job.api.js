import axios from 'axios';
import SearchJob from '../vs-entities/searchJob';

export default {
  getJobs: (state, first, number) => {
    const data = {
      state,
      first,
      number,
      sort: 'desc',
    };

    return axios.put('/api/jobs', data)
      .then(response => [{
        jobs: response.data.job !== undefined
          ? response.data.job.map(job => new SearchJob(job)) : [],
        hits: response.data.hits,
      }][0]);
  },
};
