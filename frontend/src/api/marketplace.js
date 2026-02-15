const API_BASE =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

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

// Marketplace endpoints (match your curl URL)
export const fetchMarketplaceBundles = () =>
  getJson("/marketplace/marketplace/bundles/");

// (optional) if you have this endpoint
export const fetchMarketplaceOrders = () =>
  getJson("/marketplace/marketplace/orders/");
