import React, { useContext } from 'react';
import { NavLink } from 'react-router-dom';
import ThemeContext from '../context/ThemeContext';

const Footer = () => {
  const { darkMode } = useContext(ThemeContext);

  return (
    <footer
      className={`bg-${darkMode ? 'gray-800' : 'gray-200'} text-${darkMode ? 'gray-300' : 'gray-700'}`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex justify-center">
          <NavLink
            to="/about"
            className={`mr-4 hover:text-${darkMode ? 'white' : 'black'} hover:underline transition duration-300 ease-in-out`}
          >
            About Us
          </NavLink>
          <NavLink
            to="/services"
            className={`mr-4 hover:text-${darkMode ? 'white' : 'black'} hover:underline transition duration-300 ease-in-out`}
          >
            Services
          </NavLink>
          <NavLink
            to="/contact"
            className={`hover:text-${darkMode ? 'white' : 'black'} hover:underline transition duration-300 ease-in-out`}
          >
            Contact
          </NavLink>
        </div>
        <div className="text-center mt-4">
          &copy; {new Date().getFullYear()} TradeTrendAI. All Rights Reserved.
        </div>
      </div>
    </footer>
  );
};

export default Footer;
