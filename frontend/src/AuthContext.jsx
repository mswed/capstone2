import React, { useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
import GrumpuyApi from './api';

// We create the context
const AuthContext = React.createContext();

/**
 * This is a logic only component that wraps our entire app and sets the
 * authentication context and its functions
 *
 * @param {Array}  children - Components to wrap
 * @returns {AuthContext.Provider} - with auth functions for easy access
 */

const AuthProvider = ({ children }) => {
  // We grab stuff from local storage if available
  const storedToken = localStorage.getItem('grumpy-token');
  const storedUser = localStorage.getItem('grumpy-user');

  // We set the token right away so we don't run in to authorization issues
  GrumpuyApi.token = storedToken || null;

  // Initialize state
  const [token, setToken] = useState(storedToken);
  const [currentUser, setCurrentuser] = useState(storedUser);

  // Whenever the token changes (login/logout) we need to update
  // both the api module and localStorage
  useEffect(() => {
    if (token && token.trim !== '') {
      // We only set the token if it's not empty

      GrumpuyApi.token = token;
      localStorage.setItem('grumpy-token', token || '');
      localStorage.setItem('grumpy-user', currentUser || '');
    } else {
      GrumpuyApi.token = null;
      localStorage.removeItem('grumpy-token');
      localStorage.removeItem('grumpy-user');
    }
  }, [token]);

  // TODO:
  // // We also want to get the user favorites here
  // useEffect(() => {
  //   if (!token) return;
  //   async function getUserData() {
  //     const userData = await GrumpuyApi.getUser(currentUser);
  //     setFavorites(new Set(userData.favorites));
  //   }
  //   getUserData();
  // }, [token]);

  const login = async (username, password) => {
    try {
      const authToken = await GrumpuyApi.login(username, password);
      setToken(authToken);
      const decoded = jwtDecode(authToken);
      setCurrentuser(decoded.username);
      return { success: true };
    } catch (error) {
      return { success: false, error };
    }
  };

  const register = async (username, password, firstName, lastName, email) => {
    try {
      const token = await GrumpuyApi.register(username, password, firstName, lastName, email);
      logout();
      return { success: true };
    } catch (error) {
      return { success: false, error };
    }
  };

  const logout = () => {
    // TODO: Do I need to logout of the backend here too?
    setToken('');
  };

  // TODO: We want to add favorites here
  // const addFavorite = async (jobId) => {
  //   const res = await GrumpuyApi.favoriteFormat(currentUser, jobId);
  //   if (res) {
  //     setFavorites((currentFavorites) => currentFavorites.add(res.favorites));
  //   }
  // };
  //

  // TODO: get items that have already been favorited
  // const alreadyFavorited = (formatId) => {
  //   return favFormats.has(formatId);
  // };

  // Create the value object
  const value = {
    token,
    currentUser,
    login,
    register,
    logout,
  };

  // Wrap everything in the context
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export { AuthContext, AuthProvider };
