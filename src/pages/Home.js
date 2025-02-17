import React, { useState } from "react";

function Home() {
  const [url, setUrl] = useState("");

  const handleSubmit = () => {
    alert(`Submitted URL: ${url}`);
  };

  return (
    <div className="flex items-center space-x-2 p-4">
      <input
        type="text"
        placeholder="Enter URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        className="border p-2 rounded-lg w-64"
      />
      <button
        onClick={handleSubmit}
        className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
      >
        Submit
      </button>
    </div>
  );
}

export default Home;
