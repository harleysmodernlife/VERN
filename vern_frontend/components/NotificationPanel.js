// vern_frontend/components/NotificationPanel.js
import React, { useState, useEffect } from "react";

export default function NotificationPanel() {
  const [notifications, setNotifications] = useState([]);

  // Poll for error alerts (simulated)
  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch("http://localhost:8000/notifications"); // Assume this endpoint exists
        if (res.ok) {
          const data = await res.json();
          setNotifications(data.notifications || []);
        }
      } catch (err) {
        console.error("Error fetching notifications:", err);
      }
    }, 5000); // Poll every 5 seconds

    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: "1rem", background: "#ffe", border: "1px solid #dda", borderRadius: "5px", marginTop: "1rem" }}>
      <h4>Real-Time Notifications</h4>
      {notifications.length === 0 ? (
        <p>No notifications at this time.</p>
      ) : (
        <ul>
          {notifications.map((note, idx) => (
            <li key={idx} style={{ color: note.type === "error" ? "red" : "black" }}>
              {note.message}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
