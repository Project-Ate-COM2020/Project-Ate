// import react and react router
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

// import the files for each URL endpoint
import AnalyticsPage from "./analyticsPages/analytics";
import GamePage from "./gamePages/game";
import MarketplacePage from "./marketplacePages/marketplace";
import NotFoundPage from "./reusableComponents/NotFoundPage";

// simple function defining the element to be returned based on the URL
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/game" element={<GamePage />} />
        <Route path="/marketplace" element={<MarketplacePage />} />
        <Route path="/analytics" element={<AnalyticsPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Router>
  );
}

// export the app
export default App;
