const API_BASE =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

import { getAccessToken } from "./auth";

async function getJson(path) {
  const token = getAccessToken();

  const res = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    // ✅ no cookies needed for Bearer token auth
    credentials: "omit",
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `HTTP ${res.status}`);
  }
  return res.json();
}

export const fetchMarketplaceBundles = () =>
  getJson("/marketplace/marketplace/bundles/");

export const fetchMarketplaceOrders = () =>
  getJson("/marketplace/marketplace/orders/");
