import React, { useState, useEffect } from "react";

function Home() {
  const [text, setText] = useState("");
  const [url, setUrl] = useState("");
  const [subject, setSubject] = useState("");
  const [sender, setSender] = useState("");
  const [recentScans, setRecentScans] = useState([]);
  const [score, setScore] = useState(0);

  const handleSubmit = () => {
    if (!text) {
      alert("Please enter the email text");
      return;
    }
  
    fetch(`http://3.139.235.156:8000/email/score?user_email=${encodeURIComponent(text)}&user_url=${encodeURIComponent(url)}`)
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
          subject,
          sender,
          date: new Date().toLocaleString(),
        };
  
        // setRecentScans((prevScans) => [scanResult, ...prevScans]);
        setRecentScans((prevScans) => {
          const updatedScans = [scanResult, ...prevScans];
          return updatedScans;
        });

      // Call the FastAPI /emails/ endpoint to store the email
      fetch("http://3.139.235.156:8000/emails/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_id: 1, // Replace with actual user ID
          subject,
          score: data.score,
          has_attachment: false, // Modify based on actual data
          issues: "", // Add any relevant issues if applicable
          sender,
        }),
      })
        .then((response) => response.json())
        .then((savedEmail) => {
          console.log("Email saved:", savedEmail);
        })
        .catch((error) => console.error("Error saving email:", error));

        setText(""); // Clear input field
        setUrl(""); // Clear input field
        setSubject(""); // Clear input field
        setSender(""); // Clear input field
      })
      .catch(error => console.error("Error fetching score:", error));
  };

  return (
    <div className="flex flex-col items-center p-6">
      <h2 className="text-lg font-bold mb-4">Enter Email Information</h2>
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
        <input
          type="text"
          placeholder="Enter email subject"
          value={subject}
          onChange={(e) => setSubject(e.target.value)}
          className="border p-2 rounded-lg w-full max-w-md"
        />
        <input
          type="text"
          placeholder="Enter sender's email address"
          value={sender}
          onChange={(e) => setSender(e.target.value)}
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
                <strong>{scan.subject}</strong> - {scan.sender} - {scan.status} {scan.score} ({scan.date})
              </li>
            ))
          )}
        </ul>
      </div>
    </div>
  );
}

export default Home;
