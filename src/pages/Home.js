import React, { useState, useEffect } from "react";

function Home() {
  const [text, setText] = useState("");
  const [url, setUrl] = useState("");
  const [recentScans, setRecentScans] = useState([]);
  const [score, setScore] = useState(0);

  const handleSubmit = () => {
    if (!text) {
      alert("Please enter the email text");
      return;
    }
  
    fetch(`http://127.0.0.1:8000/email/score?user_email=${encodeURIComponent(text)}&user_url=${encodeURIComponent(url)}`)
      .then(response => response.json())
      .then(data => {
        console.log("New score received:", data.score);
        setScore(data.score);
  
        // Determine status based on score ranges
        let status = "Phishing"; // Default status
        if (data.score > 50) {
          status = "Safe";
        } else if (data.score > 25) {
          status = "Suspicious";
        }

        // Create a new scan result with the updated score
        const scanResult = {
          url,
          score: data.score,
          status,
          date: new Date().toLocaleString(),
        };
  
        // setRecentScans((prevScans) => [scanResult, ...prevScans]);
        setRecentScans((prevScans) => {
          const updatedScans = [scanResult, ...prevScans];
          console.log("Updated Recent Scans:", updatedScans); // Debugging line
          return updatedScans;
        });
        setText(""); // Clear input field
        setUrl(""); // Clear input field
      })
      .catch(error => console.error("Error fetching score:", error));
  };

  return (
    <div className="flex flex-col items-center p-6">
      {/* Input Fields & Submit Button */}
      <div className="input-container">
        <textarea
          placeholder="Enter email text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          className="border p-2 rounded-lg w-full max-w-md h-32 resize-y"
        />
        <input
          type="url"
          placeholder="Enter URL to scan"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="border p-2 rounded-lg w-full max-w-md"
        />
        <button onClick={handleSubmit} className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 w-full">
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
