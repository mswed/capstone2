import React, { useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
import GrumpyApi from '../services/api';

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
  // Set up state
  const [token, setToken] = useState(null);
  const [currentUser, setCurrentuser] = useState(null);
  const [isInitialized, setIsInitialized] = useState(false);

  // We try to get the authentication from local storage once
  // and confirm we are initialized
  useEffect(() => {
    // We grab stuff from local storage if available
    const storedToken = localStorage.getItem('grumpy-token');
    const storedUser = localStorage.getItem('grumpy-user');

    if (storedToken) {
      setToken(storedToken);
      setCurrentuser(storedUser);
      GrumpyApi.token = storedToken;
    }

    setIsInitialized(true);
  }, []);

  // Whenever the token changes (login/logout) we need to update
  // both the api module and localStorage
  useEffect(() => {
    if (!isInitialized) return;

    if (token) {
      // We only set the token if it's not empty
      localStorage.setItem('grumpy-token', token || '');
      localStorage.setItem('grumpy-user', currentUser || '');
      GrumpyApi.token = token;
    } else {
      localStorage.removeItem('grumpy-token');
      localStorage.removeItem('grumpy-user');
      GrumpyApi.token = null;
    }
  }, [token, currentUser, isInitialized]);

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
      const authToken = await GrumpyApi.login(username, password);
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
      const token = await GrumpyApi.register(username, password, firstName, lastName, email);
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
    isInitialized,
  };

  // Wrap everything in the context
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export { AuthContext, AuthProvider };
