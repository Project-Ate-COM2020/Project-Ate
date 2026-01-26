// Prototype gamification page
// Shows users rescue streak, overall impact, and recent activity
// badges have been left out for now

import React, { useEffect, useState } from "react";
import { fetchGameSummary, fetchRecentRescues } from "../api/game";

export default function Game() {
  const [summary, setSummary] = useState(null);
  const [recentRescues, setRecentRescues] = useState([]);
  const [error, setError] = useState(null);

  // pull everything we need for this page
  async function load() {
    setError(null);

    try {
      const summaryResponse = await fetchGameSummary();
      const recentResponse = await fetchRecentRescues(10);
      setSummary(summaryResponse);
      setRecentRescues(Array.isArray(recentResponse) ? recentResponse : []);
    } catch (e) {
      // simplify unexpected errors for users
      setError(e instanceof Error ? e : new Error("Failed to load game data"));
    }
  }

  // load once on mount
  useEffect(() => {
    load();
  }, []);

  // early UI states

  if (error) {
    return (
      <div>
        <h2>Rescue Streaks</h2>
        <p style={{ color: "red" }}>{error.message}</p>
        <button type="button" onClick={load}>
          Try again
        </button>
      </div>
    );
  }

  if (!summary) {
    return (
      <div>
        <h2>Rescue Streaks</h2>
        <p>Loading...</p>
      </div>
    );
  }

  //  Main page UI

  return (
    <div>
      <h2>Rescue Streaks</h2>

      <section>
        <h3>Streak</h3>
        <p>
          <strong>Current streak:</strong>{" "}
          {summary.current_streak_weeks} week(s)
        </p>
        <p>
          <strong>This week:</strong>{" "}
          {summary.has_rescued_this_week ? "rescued" : " not yet"}
        </p>
      </section>

      <section>
        <h3>Personal impact</h3>
        <p>
          <strong>Total rescued bundles:</strong>{" "}
          {summary.total_rescued_bundles}
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
