import React, { useState } from "react";

const Profile= () => {
  // State for edit mode and input values
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    name: "Andre Thiel",
    email: "Roy.Doyle66@hotmail.com",
    phone: "+1 (712) 9449",
    bio: "Doloribus excepturi numquam illum voluptatem maiores. Ad illum quos tempore perspicitatis perferendis labore vitae.",
    country: "Norway",
    state: "North Carolina",
    zip: "25843",
  });

  // Handle input change
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  return (
   
      <div className="w-full  bg-white rounded-lg shadow-lg p-6">
        {/* Profile Header */}
        <div className="flex items-center border-b pb-4">
          <img
            src="https://via.placeholder.com/80"
            alt="Profile"
            className="rounded-full w-20 h-20 object-cover"
          />
          <div className="ml-4">
            <h1 className="text-2xl font-semibold text-gray-800">Account</h1>
          </div>
        </div>

        {/* Personal Details */}
        <div className="mt-6">
          <h2 className="text-lg font-medium text-gray-700 mb-2">Personal Details</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div>
              <p className="text-sm text-gray-500">Name</p>
              {isEditing ? (
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded px-2 py-1"
                />
              ) : (
                <p className="text-gray-800">{formData.name}</p>
              )}
            </div>
            <div>
              <p className="text-sm text-gray-500">Email</p>
              {isEditing ? (
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded px-2 py-1"
                />
              ) : (
                <p className="text-gray-800">{formData.email}</p>
              )}
            </div>
            <div>
              <p className="text-sm text-gray-500">Phone</p>
              {isEditing ? (
                <input
                  type="tel"
                  name="phone"
                  value={formData.phone}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded px-2 py-1"
                />
              ) : (
                <p className="text-gray-800">{formData.phone}</p>
              )}
            </div>
            <div>
              <p className="text-sm text-gray-500">Bio</p>
              {isEditing ? (
                <textarea
                  name="bio"
                  value={formData.bio}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded px-2 py-1 h-20"
                ></textarea>
              ) : (
                <p className="text-gray-800">{formData.bio}</p>
              )}
            </div>
          </div>
        </div>

        {/* Location Details */}
        <div className="mt-8">
          <h2 className="text-lg font-medium text-gray-700 mb-2">Location</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div>
              <p className="text-sm text-gray-500">Country</p>
              {isEditing ? (
                <input
                  type="text"
                  name="country"
                  value={formData.country}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded px-2 py-1"
                />
              ) : (
                <p className="text-gray-800">{formData.country}</p>
              )}
            </div>
            <div>
              <p className="text-sm text-gray-500">State</p>
              {isEditing ? (
                <input
                  type="text"
                  name="state"
                  value={formData.state}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded px-2 py-1"
                />
              ) : (
                <p className="text-gray-800">{formData.state}</p>
              )}
            </div>
            <div>
              <p className="text-sm text-gray-500">Zip/Postal Code</p>
              {isEditing ? (
                <input
                  type="text"
                  name="zip"
                  value={formData.zip}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded px-2 py-1"
                />
              ) : (
                <p className="text-gray-800">{formData.zip}</p>
              )}
            </div>
          </div>
        </div>

        {/* Edit Button */}
        <button
          onClick={() => setIsEditing(!isEditing)}
          className="mt-6 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          {isEditing ? "Save" : "Edit"}
        </button>
      </div>
   
  );
};

export default Profile;
