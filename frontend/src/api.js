import axios from 'axios';

const BASE_URL = import.meta.env.VITE_BASE_URL || 'http://127.0.0.1:8000/';

class GrumpyApi {
  static token;

  /**
   * Main API call function. This is called by the individual routes when needed
   *
   * @param {string} endpoint - the endpoint we are trying to access
   * @param {object} data - data to tranfer to the call will be converted to json
   * @param {string} method - the REST method called
   * @returns {json} - response data
   */

  static async apiCall(endpoint, data = {}, method = 'get') {
    console.debug('API CALL:', endpoint, data, method);

    const url = `${BASE_URL}/${endpoint}`;
    const headers = { Authorization: `Bearer ${GrumpyApi.token}` };
    const params = method === 'get' ? data : {};

    try {
      return (await axios({ url, method, data, params, headers })).data;
    } catch (err) {
      console.error('API Error:', err.response);
      let message = err.response.data.error.message;
      throw Array.isArray(message) ? message : [message];
    }
  }

  /*
   ****************************** Stats Routes **************************************************
   * */

  /**
   * Get basic stats
   *
   * @returns {Object} Stats of records in the database
   */

  static async getStats() {
    let res = await this.apiCall(`api/v1/stats/`);
    console.log(res);
    return res;
  }

  /*
   ****************************** Makes Routes **************************************************
   * */

  /**
   * Get all makes
   *
   * @returns {Object} All makes in the database
   */

  static async getMakes() {
    let res = await this.apiCall(`api/v1/makes/`);
    console.log(res);
    return res;
  }
}

export default GrumpyApi;
