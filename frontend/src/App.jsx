// import react and react router
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";


// import the files for each URL endpoint
import SellerSignupPage from "./authorisationPages/sellerSignupPage.jsx";
import BuyerSignupPage from "./authorisationPages/buyerSignUpPage.jsx";
import LoginPage from "./authorisationPages/loginPage.jsx";
import GamePage from "./gamePages/game";
import MarketplacePage from "./marketplacePages/marketplace";
import PageNotFound from "./reusableComponents/pageNotFound";
import UserHomePage from "./homePage/userHomePage.jsx";
//import Basket from "./Basket/basket.jsx";
import Orders from "./orders/orders.jsx"
import SellerHomePage from "./seller/homepage/main.jsx";


// simple function defining the element to be returned based on the URL
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/user" element={<UserHomePage />} />
        <Route path="/" element={<LoginPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup/buyer" element={<BuyerSignupPage />} />
        <Route path="/signup/seller" element={<SellerSignupPage />} />
        <Route path="/user" element={<UserHomePage />} />
        <Route path="/seller" element={<SellerHomePage />} />
        <Route path="/game" element={<GamePage />} />
        <Route path="/marketplace" element={<MarketplacePage />} />
        {/* <Route path="/seller/marketplace" element={<SellerMarketplace />} /> */}
        {/* <Route path="/seller/analytics" element={<AnalyticsPage />} /> */}
        {/* <Route path="/seller/forecast" element={<ForecastPage />} /> */}
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
