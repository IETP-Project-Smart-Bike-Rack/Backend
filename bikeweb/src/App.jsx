import React from 'react';
import { BrowserRouter, Route, Routes, useLocation } from 'react-router-dom';
import Home from './components/home';
import Login from './components/login';
import Signup from './components/signup';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Dashboard from './components/dashbord';
import AboutUs from './components/aboutus';

const App = () => {
  const location = useLocation(); // Hook to get the current route

  // Hide Navbar and Footer on the Dashboard route
  const hideNavAndFooter = location.pathname === '/dashboard';

  return (
    <>
      {!hideNavAndFooter && <Navbar />}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/aboutus" element={<AboutUs />} />
      </Routes>
      {!hideNavAndFooter && <Footer />}
    </>
  );
};

// Wrap App in BrowserRouter to use `useLocation`
const AppWrapper = () => (
  <BrowserRouter>
    <App />
  </BrowserRouter>
);

export default AppWrapper;
