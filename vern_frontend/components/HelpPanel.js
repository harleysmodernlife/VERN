import React from "react";

export default function HelpPanel() {
  return (
    <div style={{ border: "1px solid #0c9", padding: "2rem", borderRadius: "8px", marginTop: "2rem", background: "#f9fff9" }} role="region" aria-label="Help and Troubleshooting Panel">
      <h2 tabIndex={0} aria-label="Help and Troubleshooting">Help & Troubleshooting</h2>
      <ul>
        <li>
          <b>Missing config or API key?</b> <br />
          Check your <a href="/.env" target="_blank" rel="noopener noreferrer" aria-label="Open .env file">.env file</a> and make sure all required variables are filled in. See the <a href="/QUICKSTART.md" target="_blank" rel="noopener noreferrer" aria-label="Open Quickstart guide">Quickstart Guide</a> for details.
        </li>
        <li>
          <b>Plugin not working?</b> <br />
          Make sure the plugin is enabled in the Plugin Marketplace panel. Only supported plugins (weather, calendar, etc.) are available. See dashboard for details.
        </li>
        <li>
          <b>Workflow not running?</b> <br />
          Check that all agents in your workflow are online and configured. See the Workflow Editor panel for setup tips.
        </li>
        <li>
          <b>General troubleshooting:</b>
          <ul>
            <li>Refresh the dashboard if panels don’t load.</li>
            <li>Check browser console for errors.</li>
            <li>Contact support or submit feedback via the Feedback panel.</li>
          </ul>
        </li>
        <li>
          <b>How-to Videos:</b> <br />
          <a href="https://www.youtube.com/@vernproject" target="_blank" rel="noopener noreferrer" aria-label="Open VERN YouTube Channel">VERN YouTube Channel</a>
        </li>
        <li>
          <b>Community & Support:</b> <br />
          <a href="https://github.com/harleysmodernlife/VERN#community" target="_blank" rel="noopener noreferrer" aria-label="Join the VERN Community">Ask questions or get help in the VERN Community</a>
        </li>
      </ul>
      <div style={{ marginTop: "2rem", fontSize: "0.95em", color: "#555" }}>
        <b>FAQ:</b>
        <ul>
          <li><b>Q:</b> Why am I seeing “missing config” errors?<br /><b>A:</b> Check your .env file and fill in all required keys. See the Quickstart Guide for help.</li>
          <li><b>Q:</b> How do I enable a plugin?<br /><b>A:</b> Only supported plugins are available in the Plugin Marketplace panel.</li>
          <li><b>Q:</b> How do I get help?<br /><b>A:</b> Use this panel, the onboarding checklist, or ask in the VERN Community.</li>
        </ul>
      </div>
    </div>
  );
}
