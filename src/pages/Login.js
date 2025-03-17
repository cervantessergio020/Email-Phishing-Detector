import React, { useState } from "react";
import { useHistory } from "react-router-dom";

function Login({ setUser }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const history = useHistory();

  const handleLogin = async (e) => {
  e.preventDefault();
  try {
    const response = await fetch("http://3.139.235.156:8000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
      throw new Error("Invalid credentials");
    }

    const data = await response.json();
    setUser(data.user);
    localStorage.setItem("user", JSON.stringify(data.user));
    history.push("/");
  } catch (error) {
    alert(error.message);
  }
};

  return (
    <div className="flex flex-col items-center p-6">
      <h2 className="text-lg font-bold mb-4">Login</h2>
      <div className="input-container">
        <form className="flex flex-col space-y-2 w-64" onSubmit={handleLogin}>
          <input
            type="username"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="border p-2 rounded-lg"
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="border p-2 rounded-lg"
            required
          />
          <button
            type="submit"
            className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600"
          >
            Login
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;
