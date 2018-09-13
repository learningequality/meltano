import axios from 'axios';
import utils from './utils';

export default {
  index() {
    return axios.get(utils.buildUrl('settings'));
  },

  delete_connection(which) {
    return axios.delete(utils.buildUrl('settings/connections', `delete/${which}`));
  },

  save(data) {
    return axios.post(utils.buildUrl('settings', 'new'), data);
  },
};
