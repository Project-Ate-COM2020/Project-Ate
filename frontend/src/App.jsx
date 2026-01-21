import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import AnalyticsPage from "./analyticsPages/analytics";
import GamePage from "./gamePages/game";
import MarketplacePage from "./marketplacePages/marketplace";
import NotFoundPage from "./reusableComponents/NotFoundPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<AnalyticsPage />} />
        <Route path="/game" element={<GamePage />} />
        <Route path="/marketplace" element={<MarketplacePage />} />
        <Route path="/analytics" element={<analyticsPage />} />
        <Route path="*" element={<NotFoundPage />} /> {/* This is the pgae we show if URL doesn't exist */}
      </Routes>
    </Router>
  );
}

export default App;
