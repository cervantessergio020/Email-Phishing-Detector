import React from 'react';
import Logo from '../assets/phishlogo.png';
import { Link } from 'react-router-dom';
import '../styles/NavBar.css';

function Navbar() {
  return (
    <div className="navbar">
        <div className="leftSide">
            <img src={Logo} />
        </div>
        <div className="rightSide"></div>
          <Link to="/"> Home </Link>
          <Link to="/"> About </Link>
    </div>
  )
}

export default Navbar