import React from "react";
import Sujan from '../../assets/sujan.jpg'
import Nischal from '../../assets/nischal.jpg'

const Contact = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Meet Our Developers</h1>

      {/* Developer 1 */}
      <div className="flex items-center mb-8">
        <div className="w-1/4 mr-4">
          <img
            src={Sujan}
            alt="Sujan Bohora"
            className="rounded-full w-16 h-16"
          />
        </div>
        <div className="w-3/4">
          <h2 className="text-2xl font-semibold mb-2">Sujan Bohora</h2>
          <div className="flex">
            {/* Social media icons for Developer 1 */}
            <a href="#" className="mr-4 text-blue-500">
              <i className="fab fa-facebook"></i> {/* Facebook icon */}
            </a>
            <a href="#" className="mr-4 text-blue-500">
              <i className="fab fa-twitter"></i> {/* Twitter icon */}
            </a>
            <a href="#" className="text-blue-500">
              <i className="fab fa-linkedin"></i> {/* LinkedIn icon */}
            </a>
          </div>
        </div>
      </div>

      {/* Developer 2 */}
      <div className="flex items-center mb-8">
        <div className="w-1/4 mr-4">
          <img
            src={Nischal}
            alt="Developer 2"
            className="rounded-full w-16 h-16"
          />
        </div>
        <div className="w-3/4">
          <h2 className="text-2xl font-semibold mb-2">Nischal Rawal</h2>
          <div className="flex">
            {/* Social media icons for Developer 2 */}
            <a href="#" className="mr-4 text-blue-500">
              <i className="fab fa-facebook"></i> {/* Facebook icon */}
            </a>
            <a href="#" className="mr-4 text-blue-500">
              <i className="fab fa-twitter"></i> {/* Twitter icon */}
            </a>
            <a href="#" className="text-blue-500">
              <i className="fab fa-linkedin"></i> {/* LinkedIn icon */}
            </a>
          </div>
        </div>
      </div>

      {/* Developer 3 */}
      <div className="flex items-center">
        <div className="w-1/4 mr-4">
          <img
            src="developer3.jpg"
            alt="Developer 3"
            className="rounded-full w-16 h-16"
          />
        </div>
        <div className="w-3/4">
          <h2 className="text-2xl font-semibold mb-2">Sunil  Oli</h2>
          <div className="flex">
            {/* Social media icons for Developer 3 */}
            <a href="#" className="mr-4 text-blue-500">
              <i className="fab fa-facebook"></i> {/* Facebook icon */}
            </a>
            <a href="#" className="mr-4 text-blue-500">
              <i className="fab fa-twitter"></i> {/* Twitter icon */}
            </a>
            <a href="#" className="text-blue-500">
              <i className="fab fa-linkedin"></i> {/* LinkedIn icon */}
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Contact;
