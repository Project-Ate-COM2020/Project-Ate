import React, { useMemo } from "react";
import NavBar from "../reusableComponents/navBar";
import "./game.css";


/* --- TO USE REAL DATA: --- */
import { useGetData } from "../reusableComponents/api.jsx"

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

// memoize queryParams so useEffect doesn't trigger repeatedly
const queryParams = useMemo(() => ({}), []); // empty object, stable reference

const { data: summary, loading } = useGetData("game/summary/", queryParams, true);

  /* --- USING REAL DATA --- */

  if (loading || !summary) {
    return (
      <div className="buyer-page game-page">
        <NavBar />
        <section className="buyer-hero">
          <p className="buyer-hero-label">Impact</p>
          <h1 className="buyer-hero-title">Rescue Streaks</h1>
          <p className="buyer-hero-subtitle">Loading your impact summary…</p>
        </section>
        <div className="buyer-container game-state">
          <p className="game-subtitle">Loading…</p>
        </div>
      </div>
    );
  }

  return (
    <div className="buyer-page game-page">
      <NavBar />

      <section className="buyer-hero game-banner">
        <p className="buyer-hero-label">Impact</p>
        <h1 className="buyer-hero-title game-banner-title">Your <em>impact</em> matters.</h1>
        <p className="buyer-hero-subtitle game-banner-sub">Every bundle you rescue saves food from landfill and reduces your carbon footprint. Keep going!</p>
      </section>

      <div className="buyer-container game-wrap">
        <div className="game-impact-strip">
          <div className="game-impact-card">
            <div className="game-impact-number">{summary.total_rescued_bundles}</div>
            <div className="game-impact-unit">bundles</div>
            <div className="game-impact-label">Total Rescued</div>
          </div>
          <div className="game-impact-card">
            <div className="game-impact-number">{summary.estimated_co2e_saved_kg}<span className="game-impact-number-unit">kg</span></div>
            <div className="game-impact-unit">CO₂e saved</div>
            <div className="game-impact-label">Carbon Impact</div>
          </div>
          <div className="game-impact-card">
            <div className="game-impact-number">{summary.current_streak_weeks}</div>
            <div className="game-impact-unit">weeks</div>
            <div className="game-impact-label">Current Streak</div>
          </div>
        </div>

        <div className="game-status-pill-wrap">
          <span className="pill">
            {summary.has_rescued_this_week
              ? "Rescued this week"
              : "Not yet this week"}
          </span>
        </div>

        <div className="game-grid">
          {/* ── STREAK TRACKER ── Visual week by week streak */}
        <section className="game-card game-card--full">
          <h3>Weekly Streak</h3>
          <div className="streak-banner">
            <div>
              <div className="streak-text">
                  {summary.current_streak_weeks} week streak, keep it up!
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
           
          <section className="game-card game-card--full">
            <h3>Badges</h3>

            <ul className="badge-list">
              {Object.keys(BADGES).map((badge) => {
                const hasBadge = summary.badges.includes(badge); // check if user has it

                // Define badge requirements
                const badgeRequirements = {
                  "Explorer": { type: "categories", required: 2 },
                  "Discoverer": { type: "categories", required: 3 },
                  "Adventurer": { type: "categories", required: 4 },
                  "Master": { type: "categories", required: 6 },
                  "Eco Starter": { type: "co2", required: 100 },
                  "Eco Friend": { type: "co2", required: 500 },
                  "Climate Hero": { type: "co2", required: 1000 },
                  "Planet Saver": { type: "co2", required: 10000 },
                };

                // Compute current progress from summary
                let current = 0;
                const req = badgeRequirements[badge];
                if (req.type === "categories") {
                  current = summary.unique_categories_rescued; // how many unique badges earned so far
                } else if (req.type === "co2") {
                  current = (summary.estimated_co2e_saved_kg || 0);
                }

                const tooltipText = hasBadge
                  ? BADGES[badge].description
                  : req.type === "categories"
                    ? `${current}/${req.required} unique categories.`
                    : `${current}/${req.required}kg of CO2.`;

                return (
                  <li className="badge-item" key={badge}>
                    <div className="badge-wrapper">
                      <img
                        src={BADGES[badge].icon}
                        alt={badge}
                        className={`badge-img ${hasBadge ? "" : "badge-greyed"}`}
                      />
                      <div className="badge-tooltip">{tooltipText}</div>
                    </div>

                    <span className="badge-name">{badge}</span>
                  </li>
                );
              })}
            </ul>
          </section>

          

        </div>
      </div>
    </div>
  );
}
