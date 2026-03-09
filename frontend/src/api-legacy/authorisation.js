// Auth + shared JSON request helper in one place
export const API_BASE =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

// read a cookie value -> Django uses "csrftoken" for CSRF with session auth
function getCookie(name) {
  const cookieString = `; ${document.cookie}`;
  const parts = cookieString.split(`; ${name}=`);

  if (parts.length !== 2) return null;
  return parts.pop().split(";").shift() || null;
}

// make useful error message from common DRF response shapes
function MakeErrorMessage(statusText, data) {
  const fallback = statusText || "Request failed";

  if (!data) return fallback;
  if (typeof data === "string") return data;
  if (data.detail) return data.detail;

  // Django Rest framework validation often looks like: { field: ["msg"] }
  const firstKey = Object.keys(data)[0];
  if (!firstKey) return fallback;

  const value = data[firstKey];
  if (Array.isArray(value) && value[0]) return `${firstKey}: ${value[0]}`;
  if (typeof value === "string") return `${firstKey}: ${value}`;

  return fallback;
}

// JSON request helper that sends session cookies and CSRF token when required
export async function requestJson(path, { method = "GET", body } = {}) {
  const url = API_BASE + path;
  const headers = {};
  const hasBody = body !== undefined;

  if (hasBody) headers["Content-Type"] = "application/json";

  // attach CSRF token for non-GET requests
  const csrfToken = getCookie("csrftoken");
  if (csrfToken && method !== "GET") headers["X-CSRFToken"] = csrfToken;

  const res = await fetch(url, {
    method,
    headers,
    credentials: "include",
    body: hasBody ? JSON.stringify(body) : undefined,
  });

  // parse JSON if present -> otherwise keep data null
  let data = null;
  const contentType = res.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    try {
      data = await res.json();
    } catch {
      data = null;
    }
  }

  if (!res.ok) {
    throw new Error(MakeErrorMessage(res.statusText, data));
  }

  return data;
}

//   --------- Auth endpoints ----------

export const AUTH_ENDPOINTS = {
  login: "/api/auth/login/",
  logout: "/api/auth/logout/",
  me: "/api/auth/me/",

  // pick ONE signup approach
  signupBuyer: "/marketplace/consumer",
  signupSeller: "/api/auth/signup/seller/",
};

// Login: identifier can be email or username
export async function login({ identifier, password }) {
  return requestJson(AUTH_ENDPOINTS.login, {
    method: "POST",
    body: { identifier, password },
  });
}
export async function logout() {
  return requestJson(AUTH_ENDPOINTS.logout, { method: "POST" });
}
export async function fetchMe() {
  return requestJson(AUTH_ENDPOINTS.me, { method: "GET" });
}


// sign up functions, align payload field names with backend
export async function signupBuyer({ displayName, password }) {
  return requestJson(AUTH_ENDPOINTS.signupBuyer, {
    method: "POST",
    body: {
      display_name: displayName,
      password,
      streak: 0,
      badges: "none",
    },
  });
}

export async function signupSeller({ email, password, sellerName, location, openingHours }) {
  return requestJson(AUTH_ENDPOINTS.signupSeller, {
    method: "POST",
    body: {
      email,
      password,
      seller_name: sellerName,
      location,
      opening_hours: openingHours,
      // Removed contact_stub (phone number)
      role: "seller", // can ignore if unused
    },
  });
}
