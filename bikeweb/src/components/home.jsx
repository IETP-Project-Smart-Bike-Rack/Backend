import React from "react";
import img1 from '../assets/img1.png';
import img2 from '../assets/img2.png';
import img3 from '../assets/img3.png';
import img4 from '../assets/img4.png';
import pic1 from '../assets/pic1.jpg';
import pic2 from '../assets/pic2.jpg';
import pic3 from '../assets/pic3.png';


import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faQrcode } from "@fortawesome/free-solid-svg-icons";
import { faParking } from "@fortawesome/free-solid-svg-icons";
import { faLock } from "@fortawesome/free-solid-svg-icons";
import { faBicycle } from "@fortawesome/free-solid-svg-icons";

function Home() {
  return <>
 <div className="flex flex-wrap items-center justify-evenly gap-8 p-6 bg-white">
  {/* Left Section */}
  <div className="max-w-md align-middle m-9">
    <h1 className="text-3xl font-bold text-gray-800 text-center">Parking Area For Everyone!</h1>
    <p className="mt-4 text-gray-600 text-center">
      Cycling is not just about the journey; it’s about creating a better world one pedal at a time, and it starts with secure parking.
    </p>
  </div>

  {/* Right Section (Image) */}
  <div className="w-1/3">
    <img
      src={img1}
      alt="Bike Parking"
    />
  </div>
</div>

<div className="flex justify-evenly gap-8 p-6 bg-white overflow-x-auto">
  {/* Card 1 */}
  <div >
  <div className="bg-gray-100 p-4 rounded-lg shadow-md flex flex-col items-center justify-center text-center">
      <FontAwesomeIcon icon={faBicycle} size="3x" className="text-black mb-4" />
      <h2 className="text-xl font-semibold text-gray-800">Parking Area for Everyone</h2>
    </div>
    <div >
    <p className="mt-2 text-gray-600 text-center text-wrap">
      A convenient and accessible bike parking solution for all. Find secure, easy-to-use racks designed to make parking effortless.
    </p>
    </div>
    </div>

  {/* Card 2 */}
  <div>
  
    <div className="bg-gray-100 p-4 rounded-lg shadow-md flex flex-col items-center justify-center text-center">
    <FontAwesomeIcon icon={faQrcode} size="3x" className="text-black mb-6" />
      <h2 className="text-xl font-semibold text-gray-800">Quick QR Access</h2>
    </div>
    <div>
    <p className="mt-2 text-gray-600 text-center">
      Simply scan the QR code to lock your bike in seconds—safe, fast, and hassle-free.
    </p>
  </div>
  </div>

  {/* Card 3 */}
<div>
  

    <div className="bg-gray-100 p-4 rounded-lg shadow-md flex flex-col items-center justify-center text-center">
    <FontAwesomeIcon icon={faParking} size="3x" className="text-black mb-6" />
      <h2 className="text-xl font-semibold text-gray-800">Manage Your Rack</h2>
    </div>
    <div>
    <p className="mt-2 text-gray-600 text-center">
      View and unlock your rack anytime with a seamless, user-friendly system.
    </p>
  </div>
  </div>

  {/* Card 4 */}
  <div>
 

    <div className="bg-gray-100 p-4 rounded-lg shadow-md flex flex-col items-center justify-center text-center">
    <FontAwesomeIcon icon={faLock} size="3x" className="text-black mb-6" />
      <h2 className="text-xl font-semibold text-gray-800">Unmatched Security</h2>
    </div>
    <div>
    <p className="mt-2 text-gray-600 text-center">
      Our advanced locking mechanisms and 24/7 monitoring keep your bike safe and secure. Experience bike parking reimagined—efficient, secure, and cyclist-friendly!
    </p>
  </div>
  </div>
</div>

<div className="flex flex-wrap items-center justify-evenly gap-8 p-6 bg-white mb-9">
  {/* Left Section */}
  <div className="w-1/3">
    <img
      src={img2}
      alt="Bike Parking"
    />
  </div>

  {/* Right Section (Image) */}
  
  <div className="max-w-md ">
    <h1 className="text-3xl font-bold text-gray-800 text-center">Parking Area For Everyone!</h1>
    <p className="mt-4 text-gray-600 text-center">
      Cycling is not just about the journey; it’s about creating a better world one pedal at a time, and it starts with secure parking.
    </p>
  </div>
</div>



<div className="rounded-lg  items-center shadow-md  bg-[#addaee] from-red-300 to-green-300 w-4/6 h-60 p-8 mg-6 ml-48 ">
    <h1 className="text-center">2+ Destinations</h1>
<p className="text-center"> Transforming communities with better bicycle parking means creating spaces that are not only functional but also sustainable and welcoming. By providing secure, efficient, and innovative parking solutions, we aim to encourage cycling as a primary mode of transportation, reducing traffic congestion and promoting a healthier, greener environment. Our commitment is to design systems that integrate seamlessly into urban landscapes, making cities more bike-friendly and accessible for everyone.</p>
</div>
<div className="flex flex-wrap items-center justify-self-center -my-6 gap-4 mb-10">
  
    <img src={pic1} alt="Image 1" className="w-60 h-40 object-fit mr-10 -ml-16" />
 
  
    <img src={pic2} alt="Image 2" className="w-60 h-40 object-cover mr-7 ml-9 " />
 
 
    <img src={pic3} alt="Image 3" className="w-60 h-40 object-cover ml-9 " />
 
</div>


<div className="flex flex-wrap items-center justify-evenly gap-8 p-6 bg-gray-50 mb-10">
  {/* Left Section */}
  <div className="max-w-md">
    <h1 className="text-3xl font-bold text-gray-800 text-center">Parking Area For Everyone!</h1>
    <p className="mt-4 text-gray-600 text-center">
      Cycling is not just about the journey; it’s about creating a better world one pedal at a time, and it starts with secure parking.
    </p>
  </div>

  {/* Right Section (Image) */}
  <div className="w-1/3">
    <img
      src={img3}
      alt="Bike Parking"
    />
  </div>
</div>


<div className="flex flex-wrap items-center justify-center gap-8 p-6 bg-gradient-to-r from-gray-300 to-blue-400 rounded-lg">
  {/* Left Section */}
  <div className="w-1/2">
    <img
      src={img4}
      alt="Bike Parking"
      className="rounded-lg"
    />
  </div>

  {/* Right Section (Text) */}
  <div className="max-w-md">
    <h1 className="text-3xl font-bold text-gray-800">Parking Area For Everyone!</h1>
    <p className="mt-4 text-gray-600">
      Cycling is not just about the journey; it’s about creating a better world one pedal at a time, and it starts with secure parking.
    </p>
  </div>
</div>



  </>
}

export default Home;