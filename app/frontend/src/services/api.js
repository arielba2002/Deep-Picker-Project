// File: ./Deep-Picker-Project/app/frontend/src/services/api.js
const API_BASE_URL = 'http://localhost:8888/api/v1';

/**
 * Generic function to handle API requests
 * @param {string} endpoint - API endpoint
 * @param {string} method - HTTP method
 * @param {object} data - Request payload
 * @returns {Promise} - Promise with response data
 */
const apiRequest = async (endpoint, method = 'GET', data = null) => {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const options = {
    method,
    headers: {
      'Content-Type': 'application/json',
    },
  };

  if (data) {
    options.body = JSON.stringify(data);
  }

  const response = await fetch(url, options);
  
  // Parse response body as JSON
  const responseData = await response.json();
  
  // Handle error responses
  if (!response.ok) {
    const error = new Error(responseData.detail || 'Something went wrong');
    error.status = response.status;
    error.data = responseData;
    throw error;
  }
  
  return responseData;
};

// User API calls
export const registerUser = (userData) => {
  return apiRequest('/users/', 'POST', userData);
};

export const getUsers = (skip = 0, limit = 10) => {
  return apiRequest(`/users/?skip=${skip}&limit=${limit}`);
};

export const getUserById = (userId) => {
  return apiRequest(`/users/${userId}`);
};