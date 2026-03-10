const API_BASE =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

// reads the JWT access token stored at login
function getAccessToken() {
  return localStorage.getItem("access");
}

async function getJson(path) {
  const url = API_BASE + path;

  const res = await fetch(url, {
    credentials: "include",
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

// authenticated GET — sends JWT Bearer token when available
async function authGetJson(path) {
  const token = getAccessToken();
  const res = await fetch(API_BASE + path, {
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

// Marketplace endpoints (match your curl URL)
export const fetchMarketplaceBundles = () =>
  getJson("/marketplace/bundles/");

// kept for backwards compatibility with listings.jsx
export const fetchMarketplaceOrders = () =>
  getJson("/marketplace/orders/");

// consumer profile — GET /marketplace/consumer/<consumerId>/
// returns: { display_name, streak }
export const fetchConsumerProfile = (consumerId) =>
  authGetJson(`/marketplace/consumer/${consumerId}/`);

// consumer reservations — GET /buyer/getreservations/<consumerId>/
// returns: { reservations: [{ reservation_id, posting_id, claim_code, status, created_at }] }
export const fetchConsumerReservations = (consumerId) =>
  authGetJson(`/buyer/getreservations/${consumerId}/`);
