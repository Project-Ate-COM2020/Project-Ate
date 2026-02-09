// Prototype gamification page
// Shows users rescue streak, overall impact, and recent activity
// badges have been left out for now

import React, { useEffect, useState } from "react";
import { fetchGameSummary, fetchRecentRescues } from "../api/game";

// toggle to false when endpoints are ready
const USE_MOCK_DATA = true;

// local mock data 
const MOCK_SUMMARY = {
  current_streak_weeks: 3,
  has_rescued_this_week: true,
  total_rescued_bundles: 12,
  estimated_co2e_saved_kg: 28.5,
};

const MOCK_RECENT = [
  {
    reservation_id: 1,
    category: "Bakery",
    seller_name: "Bob Bakes",
    collected_at: "2026-01-22T17:31:00Z",
  },
  {
    reservation_id: 2,
    category: "Groceries",
    seller_name: "tesco",
    collected_at: "2026-01-18T12:10:00Z",
  },
];

export default function Game() {
  const [summary, setSummary] = useState(null);
  const [recentRescues, setRecentRescues] = useState([]);
  const [error, setError] = useState(null);

  async function load() {
    setError(null);

    try {
      if (USE_MOCK_DATA) {
        setSummary(MOCK_SUMMARY);
        setRecentRescues(MOCK_RECENT);
        return; // prevents real API calls
      }

      // backend calls (enable once Django endpoints exist)
      const summaryResponse = await fetchGameSummary();
      const recentResponse = await fetchRecentRescues(10);

      setSummary(summaryResponse);
      setRecentRescues(Array.isArray(recentResponse) ? recentResponse : []);
    } catch (e) {
      setError(e instanceof Error ? e : new Error("Failed to load game data"));
    }
  }

  useEffect(() => {
    load();
  }, []);

  // --- UI states ---
  if (error) {
    return (
      <div>
        <h2>Rescue Streaks</h2>
        <p style={{ color: "red" }}>{error.message}</p>
        <button type="button" onClick={load}>
          Try again
        </button>
        {USE_MOCK_DATA && (
          <p style={{ fontStyle: "italic" }}>
            (Dev mode: using mock data)
          </p>
        )}
      </div>
    );
  }

  if (!summary) {
    return (
      <div>
        <h2>Rescue Streaks</h2>
        <p>Loading...</p>
        {USE_MOCK_DATA && (
          <p style={{ fontStyle: "italic" }}>
            (Dev mode: using mock data)
          </p>
        )}
      </div>
    );
  }

  // --- Main page UI ---
  return (
    <div>
      <h2>Rescue Streaks</h2>

      {USE_MOCK_DATA && (
        <p style={{ fontStyle: "italic" }}>
          (Dev mode: using mock data)
        </p>
      )}

      <section>
        <h3>Streak</h3>
        <p>
          <strong>Current streak:</strong> {summary.current_streak_weeks} week(s)
        </p>
        <p>
          <strong>This week:</strong>{" "}
          {summary.has_rescued_this_week ? "rescued" : "not yet"}
        </p>
      </section>

      <section>
        <h3>Personal impact</h3>
        <p>
          <strong>Total rescued bundles:</strong> {summary.total_rescued_bundles}
        </p>
        <p>
          <strong>Estimated CO₂ saved:</strong>{" "}
          {summary.estimated_co2e_saved_kg} kg
        </p>
      </section>

      <section>
        <h3>Recent rescues</h3>

        {recentRescues.length > 0 ? (
          <ul>
            {recentRescues.map((rescue) => (
              <li key={rescue.reservation_id}>
                {rescue.category ? `${rescue.category} — ` : ""}
                {rescue.seller_name ? `${rescue.seller_name} — ` : ""}
                {rescue.collected_at
                  ? new Date(rescue.collected_at).toLocaleString()
                  : "—"}
              </li>
            ))}
          </ul>
        ) : (
          <p>No recent rescues.</p>
        )}
      </section>
    </div>
  );
}
