import React from "react";

// SVG component for Service 1
const Service1SVG = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="100"
    height="100"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    className="feather feather-airplay"
  >
    <path d="M5 11l7-7 7 7M12 18h.01" />
  </svg>
);

// SVG component for Service 2
const Service2SVG = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="100"
    height="100"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    className="feather feather-layers"
  >
    <polygon points="12 2 2 7 12 12 22 7 12 2" />
    <polyline points="2 17 12 22 22 17" />
    <polyline points="2 12 12 17 22 12" />
  </svg>
);

// SVG component for Service 3
const Service3SVG = () => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="100"
    height="100"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    className="feather feather-settings"
  >
    <circle cx="12" cy="12" r="3" />
    <path d="M19.4 15a10 10 0 0 1-2.34 2.34M4.6 15a10 10 0 0 0 2.34 2.34" />
    <path d="M21 12.3a10 10 0 0 1-1.84 1.76M4.14 10.94a10 10 0 0 1 1.72 1.84" />
    <path d="M21 9.69a10 10 0 0 0-1.76-1.84M4.14 13.06a10 10 0 0 0-1.72-1.84" />
    <path d="M12.3 21a10 10 0 0 1-1.76-1.84M10.94 4.14a10 10 0 0 1 1.84-1.72" />
  </svg>
);

const About = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Our Services</h1>

      {/* Service 1 */}
      <div className="flex items-center mb-8">
        <div className="w-1/4 mr-4">
          <Service1SVG />
        </div>
        <div className="w-3/4">
          <h2 className="text-2xl font-semibold mb-4">Stock Prediction</h2>
          <p className="text-lg text-gray-800 mb-4">
            Trade Trend provides the price forecast on each of the stock that is actively traded on the NEPSE stock exchange
          </p>
        </div>
      </div>

      {/* Service 2 */}
      <div className="flex items-center mb-8">
        <div className="w-1/4 mr-4">
          <Service2SVG />
        </div>
        <div className="w-3/4">
          <h2 className="text-2xl font-semibold mb-4">Stock Recommendation</h2>
          <p className="text-lg text-gray-800 mb-4">
            <div className="text-xl font-bold text-blue-600 mb-2"></div>
            Recommend a stock trading with similar price range and based on other similar attribute
          </p>
        </div>
      </div>

      {/* Service 3 */}
      <div className="flex items-center">
        <div className="w-1/4 mr-4">
          <Service3SVG />
        </div>
        <div className="w-3/4">
          <h2 className="text-2xl font-semibold mb-4">Provide API</h2>
          <p className="text-lg text-gray-800 mb-4">
            <div className="text-xl font-bold text-blue-600 mb-2"></div>
            our website is also capable of providing API for generating dataset which can be used to build other website and system using our data
          </p>
        </div>
      </div>
    </div>
  );
};

export default About;
