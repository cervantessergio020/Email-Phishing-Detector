import React, { useState } from "react";

function Home() {
  const [url, setUrl] = useState("");
  const [recentScans, setRecentScans] = useState([]);

  const handleSubmit = () => {
    if (!url) {
      alert("Please enter a valid URL.");
      return;
    }

    // Simulate a scan result
    const scanResult = {
      url,
      status: Math.random() > 0.5 ? "Safe" : "Phishing",
      date: new Date().toLocaleString(),
    };

    // Update the recent scans list
    setRecentScans([scanResult, ...recentScans]);
    setUrl(""); // Clear the input field
  };

  return (
    <div className="flex flex-col items-center p-6">
      {/* Input Field & Submit Button */}
      <div className="flex space-x-2 mb-6">
        <input
          type="text"
          placeholder="Enter URL to scan"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="border p-2 rounded-lg w-64"
        />
        <button
          onClick={handleSubmit}
          className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600"
        >
          Scan
        </button>
      </div>

      {/* Recent Scans List */}
      <div className="w-3/4">
        <h2 className="text-lg font-semibold mb-2">Recent Scans</h2>
        <ul className="border rounded-lg p-4 bg-gray-100">
          {recentScans.length === 0 ? (
            <p>No scans yet.</p>
          ) : (
            recentScans.map((scan, index) => (
              <li key={index} className="p-2 border-b last:border-none">
                <strong>{scan.url}</strong> - {scan.status} ({scan.date})
              </li>
            ))
          )}
        </ul>
      </div>
    </div>
  );
}

export default Home;
