const API_BASE =
  // portablitity 
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

// getting the access token 
import { getAccessToken } from "./auth"; 

// helper fucntions 
// generating with no backend 
function makeClaimCode() {
  return Math.random().toString(36).slice(2, 8).toUpperCase();
}

// Makes the fetch reques and reads the responce safely 
async function getJson(path) {
  const token = getAccessToken();

  const res = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    credentials: "omit",
  });

  const text = await res.text();
  let data;
  try { data = text ? JSON.parse(text) : null; } catch { data = text; }

  if (!res.ok) {
    throw new Error(
      typeof data === "string"
        ? data
        : (data?.detail || data?.error || JSON.stringify(data) || `HTTP ${res.status}`)
    );
  }

  return data;
}

// makes post requests  
async function postJson(path, body) {
  const token = getAccessToken();

  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    credentials: "omit",
    body: JSON.stringify(body),
  });

  const text = await res.text();
  let data;
  try { data = text ? JSON.parse(text) : null; } catch { data = text; }

  if (!res.ok) {
    throw new Error(
      typeof data === "string"
        ? data
        : (data?.detail || data?.error || JSON.stringify(data) || `HTTP ${res.status}`)
    );
  }

  return data;
}

//API Calls 

export const fetchMarketplaceBundles = () =>
  getJson("/marketplace/bundles/");

export const fetchMarketplaceOrders = () =>
  getJson("/marketplace/reservations/");

export function createReservationForPosting(postingId, consumerId) {
  return postJson("/marketplace/reservations/", {
    posting: postingId,
    consumer: consumerId,
    claim_code: makeClaimCode(),
    status: 1,
  });
}

export { API_BASE };
