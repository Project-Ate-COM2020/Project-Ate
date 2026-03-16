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
  badges: ["First Rescue", "Eco Warrior"],
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
        </div>
      </div>
    );
  }

  return (
    <div className="game-page">
      <NavBar />

{/*Dark green banner at the top of the page */}
      <div className="game-banner">
        <h1 className="game-banner-title">Your <em>impact</em> matters.</h1>
        <p className="game-banner-sub">Every bundle you rescue saves food from landfill and reduces your carbon footprint. Keep going!</p>
      </div>

      {/* Three stat cards floating over the banner */}
      <div className="game-impact-strip">
        <div className="game-impact-card">
          <div className="game-impact-number">{summary.total_rescued_bundles}</div>
          <div className="game-impact-unit">bundles</div>
          <div className="game-impact-label">Total Rescued</div>
        </div>
        <div className="game-impact-card">
          <div className="game-impact-number">{summary.estimated_co2e_saved_kg}<span style={{fontSize:"1.5rem"}}>kg</span></div>
          <div className="game-impact-unit">CO₂e saved</div>
          <div className="game-impact-label">Carbon Impact</div>
        </div>
        <div className="game-impact-card">
          <div className="game-impact-number">{summary.current_streak_weeks}</div>
          <div className="game-impact-unit">weeks</div>
          <div className="game-impact-label">Current Streak</div>
        </div>
      </div>

      <div className="game-wrap">

        <div style={{ marginBottom: 14 }}>
          <span className="pill">
            {summary.has_rescued_this_week
              ? "Rescued this week"
              : "Not yet this week"}
            {USE_MOCK_DATA ? " • Mock data" : ""}
          </span>
        </div>

        <div className="game-grid">
          {/* ── STREAK TRACKER ── Visual week by week streak */}
        <section className="game-card game-card--full">
          <h3>Weekly Streak</h3>
          <div className="streak-banner">
            <div>
              <div className="streak-text">
                  {summary.current_streak_weeks} week streak — keep it up!
              </div>
              <div className="streak-sub">
                {summary.has_rescued_this_week
                  ? " You've rescued a bundle this week!"
                  : " Rescue a bundle this week to keep your streak alive"}
              </div>
            </div>
            <div className="streak-dots">
              {Array.from({ length: 7 }, (_, i) => (
                <div key={i} className={`streak-dot ${i < summary.current_streak_weeks ? "active" : "empty"}`}>
                  W{i + 1}
                </div>
              ))}
            </div>
          </div>
        </section>

          {/* ── CO2 PROGRESS ── Shows carbon impact with a progress bar */}
        <section className="game-card game-card--full">
          <h3>Carbon Impact</h3>
          <div className="co2-display">
            <div className="co2-number">{summary.estimated_co2e_saved_kg}</div>
            <div className="co2-unit">kg of CO₂e saved so far</div>
            <div className="progress-bar-wrap">
              <div
                className="progress-bar-fill"
                style={{width: `${(summary.estimated_co2e_saved_kg / 50) * 100}%`}}
              />
            </div>
            <div className="progress-label">
              <span>0 kg</span>
              <span>{Math.round((summary.estimated_co2e_saved_kg / 50) * 100)}% to next milestone</span>
              <span>50 kg 🎯</span>
            </div>
          </div>
        </section>

          {/* ── Badges 
               ZACH TODO     : replace placeholder squares with real badge images
               each badge in summary.badges is a string name from the API
               suggested shape once assets exist
                 <img src={`/badges/${badge}.png`} alt={badge} className="badge-img" />
               The CSS class "badge-img" needs adding to game.css.
           */}
          {/* ── BADGES ── Earned badges shown as tiles, locked badges greyed out */}
        <section className="game-card game-card--full">
          <h3>Badges & Achievements</h3>

          <div className="badges-grid">
            {/* Earned badges */}
            {Array.isArray(summary.badges) && summary.badges.map((badge) => (
              <div className="badge-tile" key={badge}>
                <div className="badge-tile-name">{badge}</div>
              </div>
            ))}

            {/* Locked badges - shows what they can earn next */}
            {[
              {  name: "10 Week Streak" },
              {  name: "50kg CO₂ Saved" },
              {  name: "Top Rescuer"    },
              {  name: "25 Bundles"     },
            ].map((b) => (
              <div className="badge-tile badge-tile--locked" key={b.name}>
                <span className="badge-emoji">{b.emoji}</span>
                <div className="badge-tile-name">{b.name}</div>
              </div>
            ))}
          </div>
        </section>

        </div>
      </div>
    </div>
  );
}
