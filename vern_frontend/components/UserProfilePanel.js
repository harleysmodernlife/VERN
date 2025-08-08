// vern_frontend/components/UserProfilePanel.js
import React, { useEffect, useState } from "react";
import { IntlProvider, FormattedMessage } from "react-intl";

const messages = {
  en: {
    panelTitle: "User Profile",
    userId: "User ID",
    load: "Load",
    loading: "Loading...",
    username: "Username:",
    notFound: "User not found.",
    language: "Language"
  },
  es: {
    panelTitle: "Perfil de Usuario",
    userId: "ID de Usuario",
    load: "Cargar",
    loading: "Cargando...",
    username: "Nombre de usuario:",
    notFound: "Usuario no encontrado.",
    language: "Idioma"
  }
};

export default function UserProfilePanel() {
  const [user, setUser] = useState(null);
  const [userId, setUserId] = useState("default_user");
  const [loading, setLoading] = useState(true);
  const [locale, setLocale] = useState(() => localStorage.getItem("vern_lang") || "en");
  const [adaptationEvents, setAdaptationEvents] = useState([]);

  async function fetchUser() {
    setLoading(true);
    try {
      const res = await fetch(`http://localhost:8000/users/${userId}`);
      const data = await res.json();
      setUser(data);
    } catch (err) {
      setUser(null);
    }
    setLoading(false);
  }

  async function fetchEvents() {
    try {
      const res = await fetch(`http://localhost:8000/adaptation_events/${userId}`);
      const data = await res.json();
      setAdaptationEvents(data);
    } catch {
      setAdaptationEvents([]);
    }
  }

  useEffect(() => {
    fetchUser();
    fetchEvents();
    // eslint-disable-next-line
  }, [userId]);

  useEffect(() => {
    localStorage.setItem("vern_lang", locale);
  }, [locale]);

  return (
    <IntlProvider locale={locale} messages={messages[locale]}>
      <div style={{ border: "1px solid #888", padding: "2rem", borderRadius: "8px", marginTop: "2rem" }}>
        <div style={{ marginBottom: "1rem" }}>
          <label htmlFor="lang-select-profile" style={{ marginRight: "0.5rem" }}>
            <FormattedMessage id="language" defaultMessage="Language" />:
          </label>
          <select
            id="lang-select-profile"
            value={locale}
            onChange={e => setLocale(e.target.value)}
            aria-label="Select language"
            tabIndex={0}
            aria-describedby="lang-desc-profile"
          >
            <option value="en">English</option>
            <option value="es">Español</option>
          </select>
          <span id="lang-desc-profile" style={{ display: "none" }}>
            Choose your preferred language for the user profile panel.
          </span>
        </div>
        <h3>
          <FormattedMessage id="panelTitle" defaultMessage="User Profile" />
        </h3>
        <label>
          <FormattedMessage id="userId" defaultMessage="User ID" />:{" "}
          <input
            type="text"
            value={userId}
            onChange={e => setUserId(e.target.value)}
            style={{ width: "200px" }}
            aria-label={messages[locale].userId}
          />
          <button onClick={() => { fetchUser(); fetchEvents(); }} style={{ marginLeft: "1rem" }}>
            <FormattedMessage id="load" defaultMessage="Load" />
          </button>
        </label>
        {loading ? (
          <p><FormattedMessage id="loading" defaultMessage="Loading..." /></p>
        ) : user ? (
          <UserProfileEditor user={user} userId={userId} locale={locale} reload={() => { fetchUser(); fetchEvents(); }} />
        ) : (
          <p><FormattedMessage id="notFound" defaultMessage="User not found." /></p>
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
    </IntlProvider>
  );
}

// Editable user profile component
function UserProfileEditor({ user, userId, locale, reload }) {
  const [profile, setProfile] = useState(user.profile_data || {});
  const [username, setUsername] = useState(user.username || "");
  const [preferences, setPreferences] = useState(user.preferences || "");
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  async function saveProfile() {
    setSaving(true);
    setMessage("");
    try {
      const res = await fetch(`http://localhost:8000/users/${userId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, profile_data: profile, preferences })
      });
      const data = await res.json();
      setMessage(data.status === "updated" ? "Profile updated!" : "Error updating profile");
      reload();
    } catch (err) {
      setMessage("Error updating profile");
    }
    setSaving(false);
  }

  return (
    <div>
      <label>
        <b><FormattedMessage id="username" defaultMessage="Username:" /></b>
        <input
          type="text"
          value={username}
          onChange={e => setUsername(e.target.value)}
          style={{ marginLeft: "0.5rem", width: "200px" }}
        />
      </label>
      <div style={{ marginTop: "1rem" }}>
        <b>Preferences:</b>
        <input
          type="text"
          value={preferences}
          onChange={e => setPreferences(e.target.value)}
          style={{ marginLeft: "0.5rem", width: "300px" }}
          placeholder="e.g. dark_mode=true, notifications=off"
        />
      </div>
      <div style={{ marginTop: "1rem" }}>
        <b>Profile Data:</b>
        <textarea
          value={JSON.stringify(profile, null, 2)}
          onChange={e => {
            try {
              setProfile(JSON.parse(e.target.value));
              setMessage("");
            } catch {
              setMessage("Invalid JSON");
            }
          }}
          rows={8}
          style={{ width: "100%", background: "#f5f5f5", padding: "1rem" }}
        />
      </div>
      <button onClick={saveProfile} disabled={saving || message === "Invalid JSON"} style={{ marginTop: "1rem" }}>
        {saving ? "Saving..." : "Save"}
      </button>
      {message && (
        <div style={{ marginTop: "0.5rem", color: message.startsWith("Error") ? "red" : "green" }}>
          {message}
        </div>
      )}
      {/* TODO: Add richer preference editing and validation */}
    </div>
  );
}
