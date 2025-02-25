import React, { useState, useEffect } from "react";

function Home() {
  const [url, setUrl] = useState("");
  const [recentScans, setRecentScans] = useState([]);
  const [score, setScore] = useState(0);

  const handleSubmit = () => {
    if (!url) {
      alert("Please enter a valid URL.");
      return;
    }

    // Fetch a new score each time the button is clicked
    fetch("http://127.0.0.1:8080/email/score")
      .then(response => response.json())
      .then(data => {
        console.log("New score received:", data.score);
        setScore(data.score);

        // Create a new scan result with the updated score
        const scanResult = {
          url,
          score: data.score,
          status: data.score > 50 ? "Safe" : "Phishing",
          date: new Date().toLocaleString(),
        };

        setRecentScans([scanResult, ...recentScans]);
        setUrl(""); // Clear input field
      })
      .catch(error => console.error("Error fetching score:", error));
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
                <strong>{scan.url}</strong> - {scan.status} {scan.score} ({scan.date})
              </li>
            ))
          )}
        </ul>
      </div>
    </div>
  );
}

export default Home;
