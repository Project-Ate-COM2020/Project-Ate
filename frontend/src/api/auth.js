// api.js (or auth.js)

const API_BASE =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

// ----- Token helpers -----
export function getAccessToken() {
  return localStorage.getItem("access_token");
}

export function getRefreshToken() {
  return localStorage.getItem("refresh_token");
}

export function clearTokens() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
}

// ----- Auth: login -----
export async function login(username, password) {
  const url = new URL("/marketplace/consumer/auth/token/", API_BASE).toString();

  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
    credentials: "omit", // Bearer tokens, no cookies
  });

  if (!res.ok) throw new Error(await res.text());

  const data = await res.json();

  // Expecting SimpleJWT shape: { access: "...", refresh: "..." }
  if (!data?.access) throw new Error("Login failed: no access token returned.");

  localStorage.setItem("access_token", data.access);

  // Store refresh too (useful for debugging / later auto-refresh)
  if (data.refresh) {
    localStorage.setItem("refresh_token", data.refresh);
  } else {
    localStorage.removeItem("refresh_token");
  }

  return data;
}

// ----- Generic JSON request helper (adds Authorization correctly) -----
export async function apiJson(path, options = {}) {
  const token = getAccessToken();
  const url = new URL(path, API_BASE).toString();

  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };

  const res = await fetch(url, {
    ...options,
    headers,
    credentials: "omit",
  });

  // If token is invalid/expired, clear it so you don't keep failing forever
  if (res.status === 401) {
    clearTokens();
  }

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `HTTP ${res.status}`);
  }

  // Handle empty responses safely
  const contentType = res.headers.get("content-type") || "";
  return contentType.includes("application/json") ? res.json() : null;
}
