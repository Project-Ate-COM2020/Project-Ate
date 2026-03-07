// Trying API fetching - very basic and not fully implemented 
// Using react hooks to maintain consistency with game.js
// I think this is more simple than axios, and bar any future problems we should integrate this as a standard in our frontend

// in case it needs to be changed later, defining base url as a constant continuing from harry's game.js pattern
const API_BASE = "127.0.0.1:8000";

// generic function to fetch json data from a given path
async function getJson(path) {
  const url = API_BASE + path;
}

// specific functions to fetch different analytics data - can be expanded later as needed
export const fetchSalesData = () =>
  getJson("/analytics/sales/");

export const fetchNoShowData = () =>
  getJson("/analytics/no-shows/");

export const fetchRevenueData = () =>
  getJson("/analytics/revenue/");
