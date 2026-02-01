// import react and react router
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";


// import the files for each URL endpoint
import LoginPage from "./authorisationPages/loginPage.jsx";
import AnalyticsPage from "./analyticsPages/analytics";
import ForecastPage from "./forecastPages/forecast.jsx";
import GamePage from "./gamePages/game";
import MarketplacePage from "./marketplacePages/marketplace";
import PageNotFound from "./reusableComponents/pageNotFound";
import UserHomePage from "./homePage/userHomePage.jsx";
//import Basket from "./Basket/basket.jsx";
import Orders from "./orders/orders.jsx"
import SellerHomePage from "./homePage/sellerHomePage.jsx";
import SellerMarketplace from "./marketplacePages/sellerMarketplace.jsx";


// simple function defining the element to be returned based on the URL
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element = {<PageNotFound />} />
        <Route path="/user" element={<UserHomePage />} />
        <Route path="/seller" element={<userHomePage />} />
        <Route path="/" element={<LoginPage />} />
        <Route path="/login" element={<LoginPage />} />

        <Route path="/user" element={<UserHomePage />} />
        <Route path="/seller" element={<SellerHomePage />} />
        <Route path="/game" element={<GamePage />} />
        <Route path="/marketplace" element={<MarketplacePage />} />
        <Route path="/seller/marketplace" element={<SellerMarketplace />} />
        <Route path="/analytics" element={<AnalyticsPage />} />
        <Route path="/forecast" element={<ForecastPage />} />
        <Route path="*" element={<PageNotFound />} />
        {/*<Route path="/basket" element={<Basket />} />*/}
        <Route path="/orders" element={<Orders />}/>
      </Routes>
    </Router>
  );
}

// export the app
export default App;

// TODOS: buyer/seller is inconsistent terminology, need to replace 'user' with 'buyer' everywhere
