/**
 * base URL of the Django backend API
 *  - In development Vite injects environment variables via import.meta.env
 *  - If VITE_API_BASE_URL is not set, default to localhost:8000
 */
const API_BASE =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

// Helper function for GET requests that return JSON
async function getJson(path) {
  const url = API_BASE + path;

  const res = await fetch(url, {
    credentials: "include", // allows cookies to be sent with the request
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
  getJson("/api/game/summary/");

/**
 * Fetches recent rescued bundles for activity display
 *
 * limit prevents too many results being returned
 */
export function fetchRecentRescues(limit = 10) {
  return getJson(`/api/game/recent/?limit=${encodeURIComponent(limit)}`);
}
