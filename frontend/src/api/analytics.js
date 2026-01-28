// Trying API fetching - very basic and not fully implemented 
// Using react hooks to maintain consistency with game.js
// I think this is more simple than axios, and bar any future problems we should integrate this as a standard in our frontend

const API_BASE = "127.0.0.1:8000";

async function getJson(path) {
  const url = API_BASE + path;
}

export const fetchSalesData = () =>
  getJson("/api/analytics/sales/");

export const fetchNoShowData = () =>
  getJson("/api/analytics/no-shows/");

export const fetchRevenueData = () =>
  getJson("/api/analytics/revenue/");
