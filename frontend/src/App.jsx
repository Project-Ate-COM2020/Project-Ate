/* --- General Import Statements --- */
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";


// import the files for each URL endpoint
import SellerSignupPage from "./authorisationPages/sellerSignupPage.jsx";
import BuyerSignupPage from "./authorisationPages/buyerSignUpPage.jsx";
import SellerLoginPage from "./authorisationPages/sellerLoginPage.jsx";
import GamePage from "./gamePages/game.jsx";
import MarketplacePage from "./marketplacePages/marketplace";
import PageNotFound from "./reusableComponents/pageNotFound";
import UserHomePage from "./homePage/userHomePage.jsx";
//import Basket from "./Basket/basket.jsx";
import Orders from "./orders/orders.jsx"

/* --- Auth Imports --- */
import SellerSignupPage from "./authorisationPages/sellerSignupPage.jsx";
import BuyerSignupPage from "./authorisationPages/buyerSignupPage.jsx";

import SellerLoginPage from "./authorisationPages/sellerLoginPage.jsx";
// import BuyerLoginPage from "./authorisationPages/buyerLoginPage.jsx"

/* --- Seller Imports --- */
import SellerProfilePage from "./seller/profilePage.jsx";
import SellerHomePage from "./seller/homePage";
import CreatePostPage from "./seller/postCreation.jsx";
import Reservation from "./seller/reservation.jsx";
import Reservations from "./seller/reservations.jsx";
import Posting from "./seller/posting.jsx";
import Postings from "./seller/postings.jsx";
import Analytics from "./seller/analytics.jsx";

/* --- Buyer Imports --- */
// import BuyerProfilePage from "./buyer/profilePage.jsx";
// import BuyerHomePage from "./buyer/homePage";

// simple function defining the element to be returned based on the URL
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/user" element={<UserHomePage />} />
        {/* <Route path="/" element={<LoginPage />} /> */}
        <Route path="/login" element={<SellerLoginPage />} />
        <Route path="/buyer/login" element={<BuyerSignupPage />} />
        <Route path="/seller/login" element={<SellerLoginPage />} />
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

        {/* Seller paths */}
        <Route path="/seller/profile" element={<SellerProfilePage />}/>
        <Route path="/seller/home" element={<SellerHomePage />}/>
        <Route path="/seller/createPosting" element={<CreatePostPage />}/>
        <Route path="/seller/reservation" element={<Reservation />}/>
        <Route path="/seller/reservations" element={<Reservations />}/>
        <Route path="seller/posting" element = {<Posting />} />
        <Route path="seller/postings" element = {<Postings />} />
        <Route path="seller/analytics" element = {<Analytics />} />

        {/* Authorisation Paths */}
        <Route path="/seller/login" element={<SellerLoginPage />} />
        <Route path="/signup/buyer" element={<BuyerSignupPage />} />
        <Route path="/signup/seller" element={<SellerSignupPage />} />
      </Routes>
    </Router>
  );
}

// export the app
export default App;

// TODOS: buyer/seller is inconsistent terminology, need to replace 'user' with 'buyer' everywhere
