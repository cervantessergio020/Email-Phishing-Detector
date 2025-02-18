import React from 'react';
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import ResponsiveAppBar from './components/navbar';  // Use lowercase
import Home from './pages/Home';
import Login from './pages/Login';
import './App.css';

function App() {
  return (
    <div className="App">
      <Router>
        <ResponsiveAppBar />
        <Switch>
          <Route path="/" exact component={Home} />
          <Route path="/login" exact component={Login} />
        </Switch>
      </Router>
    </div>
  );
}

export default App;


