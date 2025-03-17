import React from "react";
import { Link, useHistory } from "react-router-dom";
import Logo from "../assets/phishlogo.png";
import "../styles/NavBar.css";

function Navbar({ user, setUser }) {
  const history = useHistory();

  const handleLogout = () => {
    setUser(null); // Clear user session
    history.push("/login"); //  Redirect to login page
  };

  return (
    <div className="navbar flex items-center justify-between p-4 bg-gray-900 text-white">
      <div className="leftSide flex items-center">
        <img src={Logo} alt="Phishing Logo" className="h-10 w-10" />
        <h1 className="text-lg font-bold ml-2">PhishScan</h1>
      </div>
      <div className="rightSide flex space-x-4">
        <Link to="/" className="hover:underline">Home</Link>

        {user ? (
          <div className="flex items-center space-x-4">
            <span className="navbar-text">{`Welcome, ${user}`}</span>
            <button
              onClick={handleLogout}
              className="bg-red-500 px-4 py-2 rounded-lg hover:bg-red-600"
            >
              Logout
            </button>
          </div>
        ) : (
          <Link to="/login" className="hover:underline">Login</Link>
        )}
      </div>
    </div>
  );
}

export default Navbar;