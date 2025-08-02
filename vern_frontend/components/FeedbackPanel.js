// vern_frontend/components/FeedbackPanel.js
import React, { useState } from "react";

export default function FeedbackPanel() {
  const [feedback, setFeedback] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [responseMsg, setResponseMsg] = useState("");

  async function submitFeedback() {
    try {
      const res = await fetch("http://localhost:8000/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ feedback })
      });
      const data = await res.json();
      setResponseMsg("Feedback submitted. Thank you!");
      setSubmitted(true);
    } catch (err) {
      setResponseMsg("Error submitting feedback.");
    }
  }

  return (
    <div style={{ border: "1px solid #ccc", padding: "1rem", borderRadius: "6px", marginTop: "1rem" }}>
      <h4>User Feedback</h4>
      {submitted ? (
        <p>{responseMsg}</p>
      ) : (
        <>
          <textarea
            value={feedback}
            onChange={e => setFeedback(e.target.value)}
            placeholder="Enter your feedback here (suggestions, bug reports, etc.)"
            style={{ width: "100%", height: "100px" }}
          />
          <br />
          <button onClick={submitFeedback} style={{ marginTop: "0.5rem" }}>
            Submit Feedback
          </button>
          {responseMsg && <p>{responseMsg}</p>}
        </>
      )}
    </div>
  );
}
