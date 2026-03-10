/**
 * base URL of the Django backend API
 *  - In development Vite injects environment variables via import.meta.env
 *  - If VITE_API_BASE_URL is not set, default to localhost:8000
 */
const API_BASE =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

// Helper to read the stored JWT access token.
// IMPORTANT: keep the key name aligned with your login implementation.
function getAccessToken() {
  // If your login stores it under a different name (e.g. "accessToken"),
  // change ONLY this line.
  return localStorage.getItem("access");
}

// Helper function for GET requests that return JSON — sends JWT token when available
async function getJson(path) {
  const url = API_BASE + path;
  const token = getAccessToken();

  const res = await fetch(url, {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  });

  if (!res.ok) {
    let message = res.statusText;
    try {
      message = (await res.json()).detail || message;
    } catch {}
    throw new Error(message);
  }
  return res.json();
}

/**
 * Fetches consumer game summary
 *
 * returns:
 *  - current streak length
 *  - total rescued bundles
 *  - CO2e estimate
 *  - badges
 */

export const fetchGameSummary = () =>
  getJson("/game/api/game/summary/");

export function fetchRecentRescues(limit = 10) {
  return getJson(`/game/api/game/recent/?limit=${encodeURIComponent(limit)}`);
}

