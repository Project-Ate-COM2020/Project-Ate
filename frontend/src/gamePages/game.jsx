import React, { useCallback, useEffect, useState } from "react";
import { fetchGameSummary, fetchRecentRescues } from "../api-legacy/game";
import NavBar from "../reusableComponents/navBar";
import "./game.css";

// toggle to false when endpoints are ready
const USE_MOCK_DATA = false;

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

  const load = useCallback(async () => {
    setError(null);

    try {
      if (USE_MOCK_DATA) {
        setSummary(MOCK_SUMMARY);
        setRecentRescues(MOCK_RECENT);
        return;
      }

      // If you ever get 401, check this in console after logging in:
      // console.log("access token:", localStorage.getItem("access"));

      const [summaryResponse, recentResponse] = await Promise.all([
        fetchGameSummary(),
        fetchRecentRescues(10),
      ]);

      setSummary(summaryResponse);
      setRecentRescues(Array.isArray(recentResponse) ? recentResponse : []);
    } catch (e) {
      // Make errors readable (fetch() errors, thrown API errors, etc.)
      const message =
        e && typeof e === "object" && "message" in e
          ? e.message
          : "Failed to load game data";

      setError(new Error(message));
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  if (error) {
    return (
      <div className="game-page">
        <NavBar />
        <div className="game-state">
          <div className="game-error">
            <h2 className="game-title">Rescue Streaks</h2>
            <p>{error.message}</p>
            <button className="game-button" type="button" onClick={load}>
              Try again
            </button>
            {USE_MOCK_DATA && (
              <p className="game-subtitle">(Dev mode: mock data)</p>
            )}
          </div>
        </div>
      </div>
    );
  }

  if (!summary) {
    return (
      <div className="game-page">
        <NavBar />
        <div className="game-state">
          <h2 className="game-title">Rescue Streaks</h2>
          <p className="game-subtitle">Loading…</p>
          {USE_MOCK_DATA && (
            <p className="game-subtitle">(Dev mode: mock data)</p>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="game-page">
      <NavBar />

      <div className="game-wrap">
        <header className="game-header">
          <h2 className="game-title">Rescue Streaks</h2>
          <p className="game-subtitle">
            Track your streak, your impact, and your recent rescues.
          </p>
        </header>

        <div style={{ marginBottom: 14 }}>
          <span className="pill">
            {summary.has_rescued_this_week
              ? "Rescued this week"
              : "Not yet this week"}
            {USE_MOCK_DATA ? " • Mock data" : ""}
          </span>
        </div>

        <div className="game-grid">
          <section className="game-card">
            <h3>Streak</h3>

            <div className="stat-row">
              <span className="stat-label">Current streak</span>
              <span className="stat-value">
                {summary.current_streak_weeks} week(s)
              </span>
            </div>

            <div className="stat-row">
              <span className="stat-label">This week</span>
              <span className="stat-value">
                {summary.has_rescued_this_week ? "rescued" : "not yet"}
              </span>
            </div>
          </section>

          <section className="game-card">
            <h3>Personal impact</h3>

            <div className="stat-row">
              <span className="stat-label">Total rescued bundles</span>
              <span className="stat-value">{summary.total_rescued_bundles}</span>
            </div>

            <div className="stat-row">
              <span className="stat-label">Estimated CO₂ saved</span>
              <span className="stat-value">
                {summary.estimated_co2e_saved_kg} kg
              </span>
            </div>
          </section>

          <section className="game-card recent">
            <h3>Recent rescues</h3>

            {recentRescues.length > 0 ? (
              <ul className="recent-list">
                {recentRescues.map((rescue) => (
                  <li className="recent-item" key={rescue.reservation_id}>
                    <span className="stat-value">
                      {rescue.category ? `${rescue.category}` : "Rescue"}
                    </span>
                    <span className="stat-label">
                      {rescue.seller_name ? ` • ${rescue.seller_name}` : ""}
                      {rescue.collected_at
                        ? ` • ${new Date(rescue.collected_at).toLocaleString()}`
                        : ""}
                    </span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="game-subtitle">No recent rescues.</p>
            )}
          </section>
        </div>
      </div>
    </div>
  );
}
