import React from "react";


export default function Signup() {
    return (
      
        <div className="min-h-screen flex items-center justify-center bg-gray-100">
  <form className="bg-white p-8 rounded-lg shadow-md w-1/2">
    <h1 className="text-2xl font-semibold text-gray-900 mb-6">
      Create your profile
    </h1>

    {/* Category and Upload ID */}
    <div className="grid grid-cols-2 gap-4 mb-4">
      <div>
        <label className="block text-sm font-medium text-maroon-800 mb-1">
          Category
        </label>
        <select
          className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option>Addis Ababa</option>
          <option>Hawassa</option>
          <option>Adama</option>
        </select>
      </div>
      <div>
        <label className="block text-sm font-medium text-maroon-800 mb-1">
          Upload ID
        </label>
        <div className="flex items-center space-x-2">
          
          <input
            type="file"
            className="w-full text-gray-500 px-2 py-1 border border-gray-300 rounded-md focus:outline-none"
          
          />
        </div>
      </div>
    </div>

    {/* Address and Phone Number */}
    <div className="grid grid-cols-2 gap-4 mb-4">
      <div>
        <label className="block text-sm font-medium text-maroon-800 mb-1">
          Address
        </label>
        <input
          type="text"
          className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-maroon-800 mb-1">
          Phone Number
        </label>
        <input
          type="text"
          className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
    </div>

    {/* Email */}
    <div className="mb-4">
      <label className="block text-sm font-medium text-maroon-800 mb-1">
        Email
      </label>
      <input
        type="email"
        className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>

    {/* Description */}
    <div className="mb-4">
      <label className="block text-sm font-medium text-maroon-800 mb-1">
        Description
      </label>
      <textarea
        className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 h-32"
      ></textarea>
    </div>

    {/* Submit Button */}
    <button
      type="submit"
      className="w-full bg-black text-white py-2 rounded-md hover:bg-gray-800"
    >
      Sign Up
    </button>
  </form>
</div>

      
    );
  }
  