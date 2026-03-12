import React, { useCallback, useEffect, useState } from "react";
import { fetchGameSummary } from "../api-legacy/game";
import NavBar from "../reusableComponents/navBar";
import "./game.css";

// toggle to false when endpoints are ready
const USE_MOCK_DATA = true;

// local mock data
const MOCK_SUMMARY = {
  current_streak_weeks: 3,
  has_rescued_this_week: true,
  total_rescued_bundles: 12,
  estimated_co2e_saved_kg: 28.5,
  // badges comes from GET /game/api/game/summary/ — array of badge name strings
  // TODO: swap these for real badge objects once the badge images/assets are decided
  badges: ["Explorer", "Eco Starter"],
};

const BADGES = {
  "Explorer": {
    icon: "/badges/explorer.png",
    description: "Rescued 2 different food categories."
  },
  "Discoverer": {
    icon: "/badges/discoverer.png",
    description: "Rescued 3 different food categories."
  },
  "Adventurer": {
    icon: "/badges/adventurer.png",
    description: "Rescued 4 different food categories."
  },
  "Master": {
    icon: "/badges/master.png",
    description: "Rescued all 6 food categories."
  },

  "Eco Starter": {
    icon: "/badges/eco_starter.png",
    description: "Saved 100kg of CO₂ by rescuing food."
  },
  "Eco Friend": {
    icon: "/badges/eco_friend.png",
    description: "Saved 500kg of CO₂ by rescuing food."
  },
  "Climate Hero": {
    icon: "/badges/climate_hero.png",
    description: "Saved 1,000kg of CO₂ by rescuing food."
  },
  "Planet Saver": {
    icon: "/badges/planet_saver.png",
    description: "Saved 10,000kg of CO₂ by rescuing food."
  }
};

export default function Game() {
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState(null);

  const load = useCallback(async () => {
    setError(null);

    try {
      if (USE_MOCK_DATA) {
        setSummary(MOCK_SUMMARY);
        return;
      }

      // If you ever get 401, check this in console after logging in:
      // console.log("access token:", localStorage.getItem("access"));

      const summaryResponse = await fetchGameSummary();
      setSummary(summaryResponse);
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
            Track your streak, your impact, and your badges.
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

          {/* ── Badges 
               ZACH TODO     : replace placeholder squares with real badge images
               each badge in summary.badges is a string name from the API
               suggested shape once assets exist
                 <img src={`/badges/${badge}.png`} alt={badge} className="badge-img" />
               The CSS class "badge-img" needs adding to game.css.
           */}
          <section className="game-card game-card--full">
            <h3>Badges</h3>

            {Array.isArray(summary.badges) && summary.badges.length > 0 ? (
              <ul className="badge-list">
                {summary.badges.map((badge) => (
                  <li className="badge-item" key={badge}>
                    <div className="badge-wrapper">
                      <img
                        src={BADGES[badge]?.icon || "/badges/default.png"}
                        alt={badge}
                        className="badge-img"
                      />

                      <div className="badge-tooltip">
                        {BADGES[badge]?.description || "Badge description"}
                      </div>
                    </div>

                    <span className="badge-name">{badge}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="game-subtitle">
                No badges yet — keep rescuing bundles to earn them.
              </p>
            )}
          </section>

        </div>
      </div>
    </div>
  );
}
