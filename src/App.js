import React, { useState } from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import ResponsiveAppBar from "./components/navbar";
import Home from "./pages/Home";
import Login from "./pages/Login";
import "./App.css";

function App() {
  const [user, setUser] = useState(null); // Track the logged-in user

  return (
    <div className="App">
      <Router>
        {/* Pass BOTH user and setUser to Navbar */}
        <ResponsiveAppBar user={user} setUser={setUser} />
        <Switch>
          <Route path="/" exact component={Home} />
          <Route path="/login" exact>
            <Login setUser={setUser} /> {/* Pass setUser to Login */}
          </Route>
        </Switch>
      </Router>
    </div>
  );
}

export default App;