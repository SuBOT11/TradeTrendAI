import React, { useState } from 'react';
import axios from 'axios';
import {Redirect, useAsyncError, useNavigate} from 'react-router-dom';
import { data } from 'autoprefixer';

const LoginSignup = () => {
  const [loginOrSignup, setLoginOrSignup] = useState('');
  const [message,setMessage]  = useState('');
  const [error , setError] = useState('');
  const navigate = useNavigate();

  const [data, setData] = useState({
	firstName: "",
	lastName: "",
	email: "",
	password: "",
	});
  	const handleChange = ({ currentTarget: input }) => {
		setData({ ...data, [input.name]: input.value });
	};

  const handleChoiceChange = (e) => {
    setLoginOrSignup(e.target.value);
  };

  const handleSignupSubmit= async (e) => {
    e.preventDefault();
    // Send login request to backend
    try {
			const url = "http://localhost:5000/api/auth/register";
			const { data: res } = await axios.post(url, data
        );
			localStorage.setItem("token", res.data);
      setMessage("successfully registered")
			window.location = "/login";
			
		} catch (error) {
			if (
				error.response &&
				error.response.status >= 400 &&
				error.response.status <= 500
			) {
				setError(error.response.data.message);
			}
		}
    
  };

  const handleLoginSubmit= async(e) => {
    e.preventDefault();
    // Send signup request to backend

    try {
			const url = "http://localhost:5000/api/auth/login";
			const { data: res } = await axios.post(url,{username : data['username'],
      password : data['password']}

      );
			localStorage.setItem("token", res.data);
      window.location('/');
			
		} catch (error) {
			if (
				error.response &&
				error.response.status >= 400 &&
				error.response.status <= 500
			) {
				setError(error.response.data.message);
			}
      
		}
    
  };

  return (
    <div className="flex justify-center items-center h-screen">
      <div className="w-full max-w-md bg-white shadow-md rounded px-8 pt-6 pb-8">
        <h2 className="text-2xl mb-4 text-center font-bold">Welcome</h2>
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="choice">
            Are you a new user?
          </label>
          <div className="flex items-center">
            <input
              className="mr-2 leading-tight"
              type="radio"
              id="login"
              name="choice"
              value="login"
              checked={loginOrSignup === 'login'}
              onChange={handleChoiceChange}
            />
            <label className="text-sm" htmlFor="login">
              Login
            </label>
          </div>
          <div className="flex items-center mt-2">
            <input
              className="mr-2 leading-tight"
              type="radio"
              id="signup"
              name="choice"
              value="signup"
              checked={loginOrSignup === 'signup'}
              onChange={handleChoiceChange}
            />
            <label className="text-sm" htmlFor="signup">
              Sign Up
            </label>
          </div>
        </div>
        {loginOrSignup && (
          <>
          <form onSubmit={loginOrSignup === 'login' ? handleLoginSubmit : handleSignupSubmit}>
            {loginOrSignup === 'signup' && (
              <>
                <div className="mb-4">
                  <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="firstName">
                    First Name
                  </label>
                  <input
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    id="firstName"
                    onChange={handleChange}
                    value={data.firstName}
                    type="text"
                    placeholder="First Name"
                  />
                </div>
                <div className="mb-4">
                  <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="lastName">
                    Last Name
                  </label>
                  <input
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    id="lastName"
                    onChange={handleChange}
                    value={data.lastName}
                    type="text"
                    placeholder="Last Name"
                  />
                </div>
              </>
            )}
            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="username">
                Username
              </label>
              <input
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                id="username"
                onChange={handleChange}
                value={data.username}
                type="text"
                placeholder="Username"
              />
            </div>
            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="email">
                Email
              </label>
              <input
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                id="email"
                onChange={handleChange}
                value={data.email}
                type="email"
                placeholder="Email"
              />
            </div>
            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="password">
                Password
              </label>
              <input
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                id="password"
                onChange={handleChange}
                value={data.password}
                type="password"
                placeholder="Password"
              />
            </div>
            {loginOrSignup === 'signup' && (
              <div className="mb-4">
                <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="confirmPassword">
                  Confirm Password
                </label>
                <input
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                  id="confirmPassword"
                  onChange={handleChange}
                  value={data.confirmPassword}
                  type="password"
                  placeholder="Confirm Password"
                />
              </div>
            )}
            <button
              className="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              type="submit"
            >
              {loginOrSignup === 'login' ? 'Login' : 'Sign Up'}
            </button>
          </form>
          <p>{message}</p>
          </>
        )}
        <p className="text-center text-gray-500 text-xs">
          &copy;2024 Acme Corp. All rights reserved.
        </p>
      </div>
    </div>
  );
};

export default LoginSignup;
