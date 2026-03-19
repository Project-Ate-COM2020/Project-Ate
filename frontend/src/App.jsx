/* --- General Import Statements --- */
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";


// import the files for each URL endpoint
import Orders from "./buyer/orders.jsx";
import LoginPage from "./authorisationPages/loginPage.jsx";
import GamePage from "./gamePages/game.jsx";
import MarketplacePage from "./buyer/marketplace.jsx";
import PageNotFound from "./reusableComponents/pageNotFound.jsx";
import UserHomePage from "./homePage/userHomePage.jsx";
import HomePage from "./homePage/HomePage.jsx";
//import Basket from "./Basket/basket.jsx";

/* --- Auth Imports --- */
import SellerSignupPage from "./authorisationPages/sellerSignupPage.jsx";
import BuyerSignupPage from "./authorisationPages/buyerSignupPage.jsx";

// import SellerLoginPage from "./authorisationPages/sellerLoginPage.jsx";
// import BuyerLoginPage from "./authorisationPages/buyerLoginPage.jsx"

/* --- Seller Imports --- */
import SellerProfilePage from "./seller/profilePage.jsx";
import SellerHomePage from "./seller/homePage.jsx";
import CreatePostPage from "./seller/postCreation.jsx";
import Reservation from "./seller/reservation.jsx";
import Reservations from "./seller/reservations.jsx";
import Posting from "./seller/posting.jsx";
import Postings from "./seller/postings.jsx";
import Analytics from "./seller/analytics.jsx";

/* --- Buyer Imports --- */
// import BuyerProfilePage from "./buyer/profilePage.jsx";
// import BuyerHomePage from "./buyer/homePage";
import BuyerProfilePage from "./buyer/BuyerProfilePage.jsx";
import IssueReportingPage from "./buyer/issueReportingPage.jsx";
import SellerIssuesPage from "./seller/sellerIssuesPage.jsx";

/* --- Webpage Imports --- */

import CookiesConsent from "./cookiePopup/cookiesConsent";
import TermsAndConditions from "./cookiePopup/TermsAndConditions";
import CookiePolicy from "./cookiePopup/CookiePolicy";
import FootNote from "./reusableComponents/footnote";
import PrivacyPolicy from "./reusableComponents/privacyPolicy";

// simple function defining the element to be returned based on the URL
function App() {
  return (
    <Router>
      
      <CookiesConsent />

      <Routes>
        {/* Public / auth paths */}
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/seller/login" element={<LoginPage />} />
        {/*<Route path="/" element={<LoginPage />} />*/}
        {/*<Route path="/login" element={<LoginPage />} />*/}
        {/*<Route path="/seller/login" element={<LoginPage />} />*/}
        <Route path="/signup/buyer" element={<BuyerSignupPage />} />
        <Route path="/signup/seller" element={<SellerSignupPage />} />
        <Route path="/user" element={<HomePage />} />
        <Route path="/seller" element={<SellerHomePage />} />
        <Route path="/game" element={<GamePage />} />
        <Route path="/buyer-profile" element={<BuyerProfilePage />} />
        {/*<Route path="/buyer-profile" element={<BuyerProfilePage />} />
        <Route path="/buyer-profile" element={<BuyerProfilePage />} />
        <Route path="/buyer-profile" element={<BuyerProfilePage />} /> */}
        {/* <Route path="/seller/marketplace" element={<SellerMarketplace />} /> */}
        {/* <Route path="/seller/analytics" element={<AnalyticsPage />} /> */}
        {/* <Route path="/seller/forecast" element={<ForecastPage />} /> */}
        <Route path="*" element={<PageNotFound />} />
        <Route path="/signup/buyer" element={<BuyerSignupPage />} />
        <Route path="/signup/seller" element={<SellerSignupPage />} />

        {/* Buyer paths */}
        <Route path="/buyer/home" element={<UserHomePage />} />
        <Route path="/buyer/profile" element={<BuyerProfilePage />} />
        <Route path="/buyer/orders" element={<Orders />} />
        <Route path="/buyer/report-issue" element={<IssueReportingPage />} />
        <Route path="/game" element={<GamePage />} />
        {/*<Route path="/basket" element={<Basket />} />*/}

        {/* Seller paths */}
        <Route path="/seller/home" element={<SellerHomePage />} />
        <Route path="/seller/profile" element={<SellerProfilePage />} />
        <Route path="/seller/createPosting" element={<CreatePostPage />} />
        <Route path="/seller/reservation" element={<Reservation />} />
        <Route path="/seller/reservations" element={<Reservations />} />
        <Route path="/seller/posting" element={<Posting />} />
        <Route path="/seller/postings" element={<Postings />} />
        <Route path="/seller/analytics" element={<Analytics />} />
        <Route path="/seller/issues" element={<SellerIssuesPage />} />

        {/* Legal pages */}
        <Route path="/terms-and-conditions" element={<TermsAndConditions />} />
        <Route path="/cookie-policy" element={<CookiePolicy />} />
        <Route path="/privacy-policy" element={<PrivacyPolicy />} />

        <Route path="*" element={<PageNotFound />} />
      </Routes>

      <FootNote />

    </Router>
  );
}

// export the app
export default App;

// buyer/seller terminology is now consistent - 'user' replaced with 'buyer' throughout
