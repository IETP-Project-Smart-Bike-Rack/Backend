import React from "react";
import group from '../assets/group.png'
const AboutUs = () => {
  return (
    <div className="bg-gray-50 min-h-screen flex  items-center justify-around">
      
        
          
          <div className=" text-wrap w-1/2">
            <h2 className="text-4xl font-bold text-gray-800 mb-4">About Us</h2>
            <p className="text-gray-600 leading-relaxed mb-6 text-balance">
            We are IETP Group 73, a dedicated team focused on developing innovative smart bike rack solutions. Our mission is to enhance urban mobility by providing efficient, secure, and technologically advanced bike parking systems. Combining our passion for technology with real-world problem-solving, we aim to create smarter, greener cities where cycling becomes a convenient and sustainable mode of transportation. By leveraging cutting-edge tools and collaborative teamwork, we strive to deliver impactful solutions that benefit both communities and the environment.
            </p>
          </div>

        
          <div className="flex justify-center">
            <img
              src={group} // Replace with your image path
              alt="About Us Illustration"
              className="w-full max-w-md"
            />
          </div>

        </div>
      
   
  );
};

export default AboutUs;
