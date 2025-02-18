import React from 'react';
import { Link } from 'react-router-dom';
import Logo from '../assets/phishlogo.png';
import '../styles/NavBar.css';

function Navbar() {
  return (
    <div className="navbar flex items-center justify-between p-4 bg-gray-900 text-white">
      <div className="leftSide flex items-center">
        <img src={Logo} alt="Phishing Logo" className="h-10 w-10" />
        <h1 className="text-lg font-bold ml-2">PhishScan</h1>
      </div>
      <div className="rightSide flex space-x-4">
        <Link to="/" className="hover:underline">Home</Link>
        <Link to="/login" className="hover:underline">Login</Link>
      </div>
    </div>
  );
}

export default Navbar;
