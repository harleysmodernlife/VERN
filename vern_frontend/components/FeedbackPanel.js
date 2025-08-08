// vern_frontend/components/FeedbackPanel.js
import React, { useState, useEffect } from "react";

export default function FeedbackPanel() {
  const [feedback, setFeedback] = useState("");
  const [feedbackType, setFeedbackType] = useState("general");
  const [userId, setUserId] = useState("default_user");
  const [submitted, setSubmitted] = useState(false);
  const [responseMsg, setResponseMsg] = useState("");
  const [adaptationEvents, setAdaptationEvents] = useState([]);

  useEffect(() => {
    async function fetchEvents() {
      try {
        const res = await fetch(`http://localhost:8000/adaptation_events/${userId}`);
        const data = await res.json();
        setAdaptationEvents(data);
      } catch {
        setAdaptationEvents([]);
      }
    }
    fetchEvents();
    // TODO: Poll for new events or use websockets for live updates.
  }, [userId]);

  async function submitFeedback() {
    try {
      const res = await fetch("http://localhost:8000/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: userId,
          feedback_type: feedbackType,
          feedback_content: feedback
        })
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
      <label>
        User ID:
        <input
          type="text"
          value={userId}
          onChange={e => setUserId(e.target.value)}
          style={{ marginLeft: "0.5rem", width: "150px" }}
        />
      </label>
      <br />
      <label>
        Feedback Type:
        <select
          value={feedbackType}
          onChange={e => setFeedbackType(e.target.value)}
          style={{ marginLeft: "0.5rem" }}
        >
          <option value="general">General</option>
          <option value="bug">Bug</option>
          <option value="suggestion">Suggestion</option>
        </select>
      </label>
      <br />
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
      <div style={{ marginTop: "2rem" }}>
        <h5>Recent Adaptation Events</h5>
        {adaptationEvents.length === 0 ? (
          <p>No adaptation events found.</p>
        ) : (
          <ul>
            {adaptationEvents.map((event, idx) => (
              <li key={idx}>
                <b>{event.event_type}</b> - {event.event_data} <i>({event.created_at})</i>
              </li>
            ))}
          </ul>
        )}
        {/* TODO: Add filtering and richer event details */}
      </div>
    </div>
  );
}
