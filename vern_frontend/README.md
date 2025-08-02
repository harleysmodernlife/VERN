# VERN Frontend (Next.js)

This is the modern, modular, and extensible frontend for the VERN platform.  
It provides a bleeding-edge dashboard, plugin marketplace, agent/cluster visualization, onboarding, and user settings—powered by Next.js and React.

## Features

- Modular dashboard with sidebar/topbar navigation, panels, and modals
- Real-time agent/cluster status and workflow visualization (network graph, activity feed)
- Plugin management UI (list, enable/disable, install, update, logs, health)
- Marketplace browser for plugins/extensions (search, install, review)
- Live logs and diagnostics panel (filter, search, export)
- Onboarding wizard and interactive checklist
- User profile and settings (theme, accessibility, preferences)
- Accessibility: keyboard navigation, ARIA, color contrast, font scaling
- Internationalization: language selector, translation support
- Feedback and troubleshooting tools (in-app bug report, screenshot upload)
- Dark/light mode, responsive/mobile-friendly design

## Directory Structure

- `components/` - React components (dashboard, panels, widgets, etc.)
- `pages/` - Next.js pages/routes
- `public/` - Static assets (images, icons, etc.)
- `styles/` - CSS/SCSS modules and themes
- `utils/` - Helper functions and API clients
- `README.md` - This file

## Quickstart

1. Install dependencies:
   ```
   npm install
   ```
2. Run the dev server:
   ```
   npm run dev
   ```
3. Visit the app:
   ```
   http://localhost:3000
   ```

## API Usage & Integration

- The frontend communicates with the backend FastAPI server at `http://localhost:8000`.
- All agent, plugin, and user actions are performed via REST API calls (see [vern_backend/README.md](../vern_backend/README.md)).
- API endpoints are called using fetch/axios in the frontend; see `utils/` for API clients.
- For full API docs, visit [http://localhost:8000/docs](http://localhost:8000/docs).

## Sample Workflows

- **Chat with Agents:**  
  Enter a message in the dashboard chat panel. The frontend sends it to the orchestrator API, which routes to relevant agents and returns a unified response.
- **Enable/Disable Plugins:**  
  Use the Plugin Registry panel to toggle tools. The frontend updates plugin state via the backend API.
- **User Profile:**  
  Load and update your profile in the User Profile panel. Changes are sent to the backend and persisted in the database.
- **Onboarding:**  
  Complete the onboarding wizard to set preferences and initialize your user profile.

## Testing & CI

- Run all frontend tests (if present):
  ```
  npm test
  ```
- Manual testing: Open the dashboard and try each panel. Check browser console and backend logs for errors.
- CI/CD: Add your preferred workflow (GitHub Actions, Vercel, etc.) to automate tests and deploy on push/PR.

## See Also

- [vern_backend/README.md](../vern_backend/README.md)
- [../README.md](../README.md)
