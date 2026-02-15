// authentication Manual 

// allow portablity due to VITE
const API_BASE =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

// local storage for access tokens and the abitlity to clear them 
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

//login / get the tokens 
export async function login(username, password) {
  const url = new URL("/marketplace/consumer/auth/token/", API_BASE).toString();

  // sending a post request to the backend to get the tockens 
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
    credentials: "omit", // Bearer tokens, no cookies
  });

  if (!res.ok) throw new Error(await res.text());

  const data = await res.json(); // tokens recived 

  // check the bankend returend what I expected 
  if (!data?.access) throw new Error("Login failed: no access token returned.");

  localStorage.setItem("access_token", data.access);

  // IDK if we use a refesh token or no so either stored or don't store it 
  if (data.refresh) {
    localStorage.setItem("refresh_token", data.refresh);
  } else {
    localStorage.removeItem("refresh_token");
  }

  return data;
}

// Automatically looks up access tokens so you can test the side without beign logged in 
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

  // If token is invalid/expired it clears them to stop you from failing 
  if (res.status === 401) {
    clearTokens();
  }

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `HTTP ${res.status}`);
  }

  // Handle empty responses 
  const contentType = res.headers.get("content-type") || "";
  return contentType.includes("application/json") ? res.json() : null;
}
