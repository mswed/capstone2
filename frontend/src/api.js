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
   * @returns {Array} All makes in the database
   */

  static async getMakes() {
    let res = await this.apiCall(`api/v1/makes/`);
    return res;
  }

  /**
   * Get make details
   *
   * @returns {Object} Full make details including related cameras
   */

  static async getMakeDetails(makeId) {
    let res = await this.apiCall(`api/v1/makes/${makeId}`);
    return res;
  }

  /*
   ****************************** Camera Routes **************************************************
   * */

  /**
   * Get all cameras
   *
   * @returns {Array} All cameras in the database
   */

  static async getCameras() {
    let res = await this.apiCall(`api/v1/cameras/`);
    return res;
  }

  /**
   * Search cameras
   *
   * @returns {Array} Found cameras in the database or an empty list
   */

  static async findCameras(query = '') {
    console.log('query is', query);
    if (!query) {
      // No search was provided
      return [];
    }
    const q = query;
    console.log('q is set to ', q);
    let res = await this.apiCall(`api/v1/cameras/search`, { q });

    return res;
  }

  /**
   * Get camera details
   *
   * @param {Integer} cameraId - The camera id to search for
   * @returns {Object} Full camera details including formats
   */

  static async getCameraDetails(cameraId) {
    let res = await this.apiCall(`api/v1/cameras/${cameraId}`);
    console.log('API RESPONDED WITH', res);
    return res;
  }

  /*
   ****************************** Format Routes **************************************************
   * */

  /**
   * Get format details
   *
   * @param {Integer} formatId - The format id to search for
   * @returns {Object} Full forat details
   */

  static async getFormatDetails(formatId) {
    let res = await this.apiCall(`api/v1/formats/${formatId}`);
    console.log('API RESPONDED WITH', res);
    return res;
  }

  /**
   * Get all formats
   *
   * @returns {Array} All of the formats in the database
   */

  static async getFormats() {
    let res = await this.apiCall(`api/v1/formats/`);
    return res;
  }

  /**
   * Search formats
   *
   * @returns {Array} Found formats in the database or an empty list
   */

  static async findFormats(query = {}) {
    console.log('query is', query);
    if (!query) {
      // No search was provided
      return [];
    }

    console.log(query);
    let res = await this.apiCall(`api/v1/formats/search`, { ...query });

    return res;
  }
}

export default GrumpyApi;
