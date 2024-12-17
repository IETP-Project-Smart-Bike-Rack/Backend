import React from "react";
import iconlogo from "../assets/logoicon.png"
import AboutUs from "./aboutus";
const Navbar = () => {
  return (
    <nav className="bg-white shadow-md py-4">
      <div className="container mx-auto px-4 flex justify-between items-center">
        {/* Logo */}
        <div className="flex items-center">
          <div className="text-2xl font-bold text-gray-800">
           <img src={iconlogo} alt="" />
          </div>
        </div>

        {/* Navigation Links */}
        <ul className="flex space-x-8 text-gray-700 font-medium">
          <li>
            <a href="./" className="hover:text-gray-900">
              Home
            </a>
          </li>
          
          <li>
            <a href="/aboutus" className="hover:text-gray-900">
              About
            </a>
          </li>
          <li>
            <a href="#footer" className="hover:text-gray-900">
              Contact us
            </a>
          </li>
        </ul>

        {/* Login Button */}
        <div className="flex items-center space-x-2">
          <div className="w-6 h-6 text-gray-600">
            <i className="far fa-user-circle text-xl"></i>
          </div>
          <a href="./login" className="text-gray-700 hover:text-gray-900 ">
            Login
          </a>
          <a href="./signup" className="text-gray-700 hover:text-gray-900 bg-blue-300 w-16 text-center rounded">
            Signup
          </a>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;