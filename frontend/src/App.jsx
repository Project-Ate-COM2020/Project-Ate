// import react and react router
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

// import the files for each URL endpoint
import AnalyticsPage from "./analyticsPages/analytics";
import GamePage from "./gamePages/game";
import MarketplacePage from "./marketplacePages/marketplace";
import PageNotFound from "./reusableComponents/pageNotFound";
import UserHomePage from "./homePage/userHomePage.jsx";
//import Basket from "./Basket/basket.jsx";
import Orders from "./orders/orders.jsx";



// simple function defining the element to be returned based on the URL
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element = {<PageNotFound />} />
        <Route path="/user" element={<UserHomePage />} />
        <Route path="/seller" element={<userHomePage />} />
        <Route path="/game" element={<GamePage />} />
        <Route path="/marketplace" element={<MarketplacePage />} />
        <Route path="/analytics" element={<AnalyticsPage />} />
        <Route path="*" element={<PageNotFound />} />
        {/*<Route path="/basket" element={<Basket />} />*/}
        <Route path="/orders" element={<Orders />}/>
      </Routes>
    </Router>
  );
}

// export the app
export default App;
