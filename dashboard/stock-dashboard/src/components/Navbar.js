import React, { useContext, useState } from 'react';
import { NavLink } from 'react-router-dom';
import ThemeContext from '../context/ThemeContext';
import Logo from '../assets/Red Illustrated Bull Stock Broker Logo (1).png';

const Navbar = () => {
  const { darkMode } = useContext(ThemeContext);
  const [showDropdown, setShowDropdown] = useState(false);

  const toggleDropdown = () => {
    setShowDropdown(!showDropdown);
  };

  return (
    <nav
      className={`bg-${darkMode ? 'gray-800' : 'gray-200'}`}
      style={{ overflow: 'visible' }} // Allow overflow
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex-shrink-0 flex items-center">
            {/* Insert logo image */}
            <img src={Logo} alt="Logo" className="h-16 py-2" />
            <span className="font-bold text-white"> TRADE TREND</span>
          </div>
          <div className="block md:hidden">
            <button
              onClick={toggleDropdown}
              className={`text-${darkMode ? 'white' : 'black'} hover:text-${
                darkMode ? 'gray-300' : 'gray-700'
              } focus:outline-none focus:text-${
                darkMode ? 'gray-300' : 'gray-700'
              }`}
            >
              <svg
                className="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                {showDropdown ? (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                ) : (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 6h16M4 12h16m-7 6h7"
                  />
                )}
              </svg>
            </button>
          </div>
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-4">
              <NavLink
                to="/"
                className={`text-${darkMode ? 'gray-300' : 'gray-700'} hover:bg-${
                  darkMode ? 'gray-700' : 'gray-300'
                } hover:text-${darkMode ? 'white' : 'black'} px-3 py-2 rounded-md text-md font-medium hover:text-gray-300 transition duration-300 ease-in-out`}
              >
                Dashboard
              </NavLink>
              <NavLink
                to="/about"
                className={`text-${darkMode ? 'gray-300' : 'gray-700'} hover:bg-${
                  darkMode ? 'gray-700' : 'gray-300'
                } hover:text-${darkMode ? 'white' : 'black'} px-3 py-2 rounded-md text-md font-medium hover:text-gray-300 transition duration-300 ease-in-out`}
              >
                About
              </NavLink>
              <NavLink
                to="/contact"
                className={`text-${darkMode ? 'gray-300' : 'gray-700'} hover:bg-${
                  darkMode ? 'gray-700' : 'gray-300'
                } hover:text-${darkMode ? 'white' : 'black'} px-3 py-2 rounded-md text-md font-medium hover:text-gray-300 transition duration-300 ease-in-out`}
              >
                Contact
              </NavLink>
            </div>
          </div>
        </div>
      </div>
      {/* Mobile dropdown */}
      {showDropdown && (
        <div className="md:hidden">
          <div className={`px-2 pt-2 pb-3 space-y-1 sm:px-3`}>
            <NavLink
              to="/"
              className={`text-${darkMode ? 'gray-300' : 'gray-700'} hover:bg-${
                darkMode ? 'gray-700' : 'gray-300'
              } hover:text-${darkMode ? 'white' : 'black'} block px-3 py-2 rounded-md text-base font-medium `}
            >
              Home
            </NavLink>
            <NavLink
              to="/about"
              className={`text-${darkMode ? 'gray-300' : 'gray-700'} hover:bg-${
                darkMode ? 'gray-700' : 'gray-300'
              } hover:text-${darkMode ? 'white' : 'black'} block px-3 py-2 rounded-md text-base font-medium `}
            >
              About
            </NavLink>
            <NavLink
              to="/services"
              className={`text-${darkMode ? 'gray-300' : 'gray-700'} hover:bg-${
                darkMode ? 'gray-700' : 'gray-300'
              } hover:text-${darkMode ? 'white' : 'black'} block px-3 py-2 rounded-md text-base font-medium `}
            >
              Services
            </NavLink>
            <NavLink
              to="/contact"
              className={`text-${darkMode ? 'gray-300' : 'gray-700'} hover:bg-${
                darkMode ? 'gray-700' : 'gray-300'
              } hover:text-${darkMode ? 'white' : 'black'} block px-3 py-2 rounded-md text-base font-medium`}
            >
              Contact
            </NavLink>
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
