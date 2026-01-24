/**
 * Gamification page (prototype scaffold)
 * Goals: (not all implemented yet)
 *  - show users rescue streak
 *  - summarise their personal impact
 *  - display recently rescued bundles
 *  - badges 
 *
 *  - this is a scaffold, UI sections are in place with TO DOs
 *  -  hook up real API calls once backend endpoints are made by backend partner
 */

import React, { useEffect, useState } from "react";
import { fetchGameSummary, fetchRecentRescues } from "../api/game";

export default function Game() {
  // state (placeholder for now)
  const [summary, setSummary] = useState(null);
  const [recentRescues, setRecentRescues] = useState([]);
  const [error, setError] = useState(null);

  /**
   * load gamification data
   * TO DO, replace when endpoints exist
   */
  function loadGameData() {
  }

  // load data when page mounts
  useEffect(() => {
  }, []);

  return (
    <div>
      <h2>Rescue Streaks</h2>

      {/* TO DO, render loading state  */}
      {/* TO DO, render error state  */}

      {/* Streaks */}
      <section>
        <h3>Streak</h3>
        {/* TO DO, show current streak (weeks) */}
        {/* TO DO, show if the user has rescued this week */}
      </section>

      {/* Impact */}
      <section>
        <h3>Personal impact</h3>
        {/* TO DO, show total rescued bundles */}
        {/* TO DO, show estimated CO2 saved */}
      </section>

      {/* Badges */}
      <section>
        <h3>Badges</h3>
        {/* TO DO, list badges/ badges to earn */}
      </section>

      {/* Recent Activity */}
      <section>
        <h3>Recent rescues</h3>
        {/* TO DO, list recent rescues */}
      </section>
    </div>
  );
}
