import axios from 'axios';
import humps, { camelizeKeys } from 'humps';

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

    if ((!data) instanceof FormData) {
      // If we are not sending FormData (i.e. uploading an image) set the type to json
      headers['Content-Type'] = 'application/json';
    } else {
    }

    const params = method === 'get' ? data : {};

    try {
      return (await axios({ url, method, data, params, headers })).data;
    } catch (err) {
      console.error('API Error:', err.response);

      // Catch connection errors
      if (!err.response) {
        throw ['Network error: unable to connect to server '];
      }
      console.log(err);
      let message = err.response.data?.error?.message || 'Something went wrong';
      throw Array.isArray(message) ? message : [message];
    }
  }

  /**
   * A helper function to format image urls. The backend returns
   * relatives paths so we need to onvert them to absolute
   * @param {Object} item - original item with a relative media path
   * @returns {Object} item with absolute path
   */

  static getAbsoluteMediaUrl = (item) => {
    if (!item) return null;
    console.log('processing item', item);

    const processedItem = { ...item };

    // media fields
    const mediaFields = ['logo', 'image'];

    // process the URL fields
    mediaFields.forEach((field) => {
      if (processedItem[field] && !processedItem[field].startsWith('http')) {
        processedItem[field] = `${BASE_URL}${processedItem[field]}`;
      }
    });

    return processedItem;
  };

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
    return humps.camelizeKeys(res);
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
    const camalized = humps.camelizeKeys(res);
    console.log('backend has these makes', camalized);
    console.log('which are now', camalized.map(this.getAbsoluteMediaUrl));

    return camalized.map(this.getAbsoluteMediaUrl);
  }

  /**
   * Get make details
   *
   * @returns {Object} Full make details including related cameras
   */

  static async getMakeDetails(makeId) {
    let res = await this.apiCall(`api/v1/makes/${makeId}`);
    const camalized = humps.camelizeKeys(res);
    console.log('original response', camalized);
    camalized['cameras'].map(this.getAbsoluteMediaUrl);
    console.log('proper camera images', camalized);

    return this.getAbsoluteMediaUrl(camalized);
  }

  /**
   * Add make. This uses FormData to submit the logo
   *
   * @param {Object} formData - The make details (name, website and logo)
   * @returns {Object}  New make details
   */

  static async addMake(formData) {
    let res = await this.apiCall(`api/v1/makes/`, formData, 'post');
    return camelizeKeys(res);
  }

  /**
   * Update make. This uses FormData to update the logo
   *
   * @param {Integer} makeId - The ID of the make we are editing
   * @param {Object} updatedData - The make details (name, website and logo)
   * @returns {Object}  Updated make details
   */

  static async updateMake(makeId, updatedData) {
    let res = await this.apiCall(`api/v1/makes/${makeId}`, updatedData, 'patch');
    const camalized = humps.camelizeKeys(res.make);

    return this.getAbsoluteMediaUrl(camalized);
  }

  /**
   * Delete make
   *
   * @param {Integer} makeId - The ID of the make we are deleting
   * @returns {Object}  Delete status
   */

  static async deleteMake(makeId) {
    let res = await this.apiCall(`api/v1/makes/${makeId}`, {}, 'delete');
    return humps.camelizeKeys(res);
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
    const camalized = humps.camelizeKeys(res);
    console.log('backend has these cameras', camalized);
    console.log('which are now', camalized.map(this.getAbsoluteMediaUrl));
    return camalized.map(this.getAbsoluteMediaUrl);
  }

  /**
   * Search cameras
   *
   * @returns {Array} Found cameras in the database or an empty list
   */

  static async findCameras(query = '') {
    if (!query) {
      // No search was provided
      return [];
    }
    const q = query;
    let res = await this.apiCall(`api/v1/cameras/search`, { q });

    const camalized = humps.camelizeKeys(res);
    return camalized.map(this.getAbsoluteMediaUrl);
  }

  /**
   * Get camera details
   *
   * @param {Integer} cameraId - The camera id to search for
   * @returns {Object} Full camera details including formats
   */

  static async getCameraDetails(cameraId) {
    let res = await this.apiCall(`api/v1/cameras/${cameraId}`);
    const camalized = humps.camelizeKeys(res);
    console.log('backend has this amera', camalized);
    console.log('which is now now', this.getAbsoluteMediaUrl(camalized));
    return this.getAbsoluteMediaUrl(camalized);
  }

  /**
   * Create a new camera
   *
   * @param {Object} cameraData - The new camera data
   * @returns {Object} Full camera details
   */

  static async addCamera(cameraData) {
    let res = await this.apiCall(`api/v1/cameras/`, cameraData, 'post');
    return humps.camelizeKeys(res);
  }

  /**
   * Update a camera
   *
   * @param {Integer} cameraId - The ID of the camera we are updating
   * @param {object} cameraData - The updated camera data
   * @returns {Object} Full camera details
   */

  static async updateCamera(cameraId, cameraData) {
    let res = await this.apiCall(`api/v1/cameras/${cameraId}`, cameraData, 'patch');
    const camalized = humps.camelizeKeys(res.camera);

    return this.getAbsoluteMediaUrl(camalized);
  }

  /**
   * Delete camera
   *
   * @param {Integer} cameraId - The ID of the make we are deleting
   * @returns {Object}  Delete status
   */

  static async deleteCamera(cameraId) {
    let res = await this.apiCall(`api/v1/cameras/${cameraId}`, {}, 'delete');
    return humps.camelizeKeys(res.camera);
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
    return humps.camelizeKeys(res);
  }

  /**
   * Update a format
   *
   * @param {Integer} formatId - The ID of the format we are updating
   * @param {object} formatData - The updated format data
   * @returns {Object} Full format details
   */

  static async updateFormat(formatId, formatData) {
    const snakeCaseData = humps.decamelizeKeys(formatData);
    let res = await this.apiCall(`api/v1/formats/${formatId}`, snakeCaseData, 'patch');
    return humps.camelizeKeys(res.format);
  }

  /**
   * Get all formats
   *
   * @returns {Array} All of the formats in the database
   */

  static async getFormats() {
    let res = await this.apiCall(`api/v1/formats/`);
    return humps.camelizeKeys(res);
  }

  /**
   * Search formats
   *
   * @returns {Array} Found formats in the database or an empty list
   */

  static async findFormats(query = {}) {
    if (!query) {
      // No search was provided
      return [];
    }

    let res = await this.apiCall(`api/v1/formats/search`, { ...query });

    return humps.camelizeKeys(res);
  }

  /**
   * Create a new format
   *
   * @param {Object} foratData - The new format data
   * @returns {Object} Full format details
   */

  static async addFormat(formatData) {
    const snakeCaseData = humps.decamelizeKeys(formatData);
    let res = await this.apiCall(`api/v1/formats/`, snakeCaseData, 'post');
    return humps.camelizeKeys(res);
  }

  /**
   * Delete a format
   *
   * @param {Object} formatId - The id of the format to delete
   * @returns {Object}  Delete status
   */
  static async deleteFormat(formatId) {
    let res = await this.apiCall(`api/v1/formats/${formatId}`, {}, 'delete');
    return humps.camelizeKeys(res);
  }

  /*
   ****************************** Project Routes **************************************************
   * */

  /**
   * Get project details
   *
   * @param {Integer} projectId - The format id to search for
   * @returns {Object} Full forat details
   */

  static async getProjectDetails(projectId) {
    let res = await this.apiCall(`api/v1/projects/${projectId}`);
    return humps.camelizeKeys(res);
  }

  /**
   * Get all projects
   *
   * @returns {Array} All of the formats in the database
   */

  static async getProjects() {
    let res = await this.apiCall(`api/v1/projects/`);
    return humps.camelizeKeys(res);
  }

  /**
   * Delete project
   *
   * @param {Integer} projectId - The ID of the project we are deleting
   * @returns {Object}  Delete status
   */

  static async deleteProject(projectId) {
    let res = await this.apiCall(`api/v1/projects/${projectId}`, {}, 'delete');
    return humps.camelizeKeys(res);
  }

  /**
   * Search projects
   *
   * @returns {Array} Found projects in the database or an empty list
   */

  static async findProjects(query = {}) {
    if (!query) {
      // No search was provided
      return [];
    }
    const q = query;
    let res = await this.apiCall(`api/v1/projects/search`, { q });
    if (res) {
      return humps.camelizeKeys(res);
    } else {
      return [];
    }
  }

  /**
   * Add project to the database from TMDB
   *
   * @param {Integer} tmdb_id - The TMDB id of the project
   * @param {String} projectType - The project type 'feature' or 'episodic'
   * @returns {Object} success and project id if success else error
   */

  static async addTMDBProject(tmdbId, projectType) {
    let res = await this.apiCall(`api/v1/projects/`, { tmdb_id: tmdbId, project_type: projectType }, 'post');
    if (res) {
      return humps.camelizeKeys(res);
    } else {
      return [];
    }
  }

  /**
   * Add a format to a project
   *
   * @param {Integer} formatId - The format id
   * @param {Integer} projectId - The project id
   */

  static async addFormatToProject(projectId, formatId) {
    let res = await this.apiCall(`api/v1/projects/${projectId}/formats/`, { format_id: formatId }, 'post');
    if (res) {
      return humps.camelizeKeys(res);
    } else {
      return [];
    }
  }

  /**
   * Vote on a format attached to a project
   *
   * @param {Integer} formatId - The format id
   * @param {Integer} projectId - The project id
   * @param {String} vote - Vote type (up or down)
   */

  static async voteOnProjectFormat(projectId, formatId, vote) {
    let res = await this.apiCall(`api/v1/projects/${projectId}/formats/${formatId}`, { vote }, 'patch');
    if (res) {
      return humps.camelizeKeys(res);
    } else {
      return [];
    }
  }

  /*
   ****************************** Project Routes **************************************************
   * */

  /**
   * Get all sources
   *
   * @returns {Array} All sources in the database
   */

  static async getSources() {
    let res = await this.apiCall(`api/v1/sources/`);
    return humps.camelizeKeys(res);
  }

  /**
   * Create a new source
   *
   * @param {Object} sourceData - The new source data
   * @returns {Object} Full source details
   */

  static async addSource(sourceData) {
    const snakeCaseData = humps.depascalizeKeys(sourceData);
    let res = await this.apiCall(`api/v1/sources/`, snakeCaseData, 'post');
    return humps.camelizeKeys(res.source);
  }

  /**
   * Get source details
   *
   * @param {Integer} sourceId - The source id to search for
   * @returns {Object} Full source details
   */

  static async getSourceDetails(sourceId) {
    let res = await this.apiCall(`api/v1/sources/${sourceId}`);
    return humps.camelizeKeys(res);
  }

  /**
   * Update a source
   *
   * @param {Integer} sourceId - The ID of the source we are updating
   * @param {object} sourceData - The updated source data
   * @returns {Object} Full source details
   */

  static async updateSource(sourceId, sourceData) {
    const snakeCaseData = humps.decamelizeKeys(sourceData);
    let res = await this.apiCall(`api/v1/sources/${sourceId}`, snakeCaseData, 'patch');
    return humps.camelizeKeys(res.source);
  }

  /**
   * Delete a source
   *
   * @param {Object} sourceId - The id of the source to delete
   * @returns {Object}  Delete status
   */
  static async deleteSource(sourceId) {
    let res = await this.apiCall(`api/v1/sources/${sourceId}`, {}, 'delete');
    return humps.camelizeKeys(res);
  }

  /*
   ****************************** Authorization Routes **************************************************
   * */

  /**
   * Login a user
   *
   * @param {String} username - username of user
   * @param {String} password - password of user
   */
  static async login(username, password) {
    let res = await this.apiCall(`api/v1/users/auth`, { username, password }, 'post');
    GrumpyApi.token = res.token;
    return res.token;
  }

  /**
   * Signup a user
   *
   * @param {Object} userData - new user data
   */
  static async signup(userData) {
    const snakeCaseData = humps.decamelizeKeys(userData);
    let res = await this.apiCall(`api/v1/users/`, { ...snakeCaseData }, 'post');
    return humps.camelizeKeys(res);
  }

  /**
   * Logout a user
   *
   */
  static async logout() {
    let res = await this.apiCall(`api/v1/users/auth`, 'delete');
    GrumpyApi.token = res.token;
    return res.token;
  }

  /*
   ****************************** User Routes **************************************************
   * */

  /**
   * Get user details
   *
   * @param {Integer} userId - The user id to search for
   * @returns {Object} Full user details (without password, obviously)
   */

  static async getUserDetails(userId) {
    let res = await this.apiCall(`api/v1/users/${userId}`);
    console.log(res);
    return humps.camelizeKeys(res);
  }

  /**
   * Update a user
   *
   * @param {Integer} userId - The ID of the user we are updating
   * @param {object} userData - The updated user data
   * @returns {Object} Full source details
   */

  static async updateUser(userId, userData) {
    const snakeCaseData = humps.decamelizeKeys(userData);
    let res = await this.apiCall(`api/v1/users/${userId}`, snakeCaseData, 'patch');
    return humps.camelizeKeys(res.user);
  }
}

export default GrumpyApi;
