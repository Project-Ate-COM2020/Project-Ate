/* --- General Import Statements --- */
import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from "react-router-dom";
import { postData } from "./reusableComponents/api.jsx"


/* --- Auth Imports --- */
import SellerSignupPage from "./authorisationPages/sellerSignupPage.jsx";
import BuyerSignupPage from "./authorisationPages/buyerSignupPage.jsx";
import LoginPage from "./authorisationPages/loginPage.jsx";

/* --- Seller Imports --- */
import SellerProfilePage from "./seller/profile.jsx";
import SellerHomePage from "./seller/home.jsx";
import CreatePostPage from "./seller/postCreation.jsx";
import Reservations from "./seller/reservations.jsx";
import Postings from "./seller/postings.jsx";
import Analytics from "./seller/analytics.jsx";
import SellerIssuesPage from "./seller/issuesPage.jsx";

/* --- Buyer Imports --- */
import Orders from "./buyer/reservations.jsx";
import GamePage from "./buyer/game.jsx";
import BuyerProfilePage from "./buyer/profile.jsx";
import IssueReportingPage from "./buyer/issueReportingPage.jsx";
import UserHomePage from "./buyer/postings.jsx";


/* --- Global Imports --- */

import CookiesConsent from "./cookiePopup/cookiesConsent";
import TermsAndConditions from "./cookiePopup/TermsAndConditions";
import CookiePolicy from "./cookiePopup/CookiePolicy";
import FootNote from "./reusableComponents/footnote";
import PrivacyPolicy from "./reusableComponents/privacyPolicy";
import PageNotFound from "./reusableComponents/pageNotFound.jsx";
import HomePage from "./homePage/HomePage.jsx";

/* --- Maintaner Imports ---*/
import MaintenancePage from "./maintenancePage/maintenancePage.jsx";


// simple function defining the element to be returned based on the URL
function App() {
  return (
    <Router>
      
      <CookiesConsent />

      <Routes>
        {/* Auth paths */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup/buyer" element={<BuyerSignupPage />} />
        <Route path="/signup/seller" element={<SellerSignupPage />} />

        {/* Buyer paths */}
        <Route path="/buyer/home" element={<UserHomePage />} />
        <Route path="/buyer/profile" element={<BuyerProfilePage />} />
        <Route path="/buyer/orders" element={<Orders />} />
        <Route path="/buyer/report-issue" element={<IssueReportingPage />} />
        <Route path="/buyer/game" element={<GamePage />} />

        {/* Seller paths */}
        <Route path="/seller/home" element={<SellerHomePage />} />
        <Route path="/seller/profile" element={<SellerProfilePage />} />
        <Route path="/seller/createPosting" element={<CreatePostPage />} />
        <Route path="/seller/reservations" element={<Reservations />} />
        <Route path="/seller/postings" element={<Postings />} />
        <Route path="/seller/analytics" element={<Analytics />} />
        <Route path="/seller/issues" element={<SellerIssuesPage />} />

        {/* Global paths */}
        <Route path="/" element={<HomePage />} />
        <Route path="/terms-and-conditions" element={<TermsAndConditions />} />
        <Route path="/cookie-policy" element={<CookiePolicy />} />
        <Route path="/privacy-policy" element={<PrivacyPolicy />} />
        <Route path="*" element={<PageNotFound />} />

        {/* maintainer Page */}
        <Route path="/maintenance" element={<MaintenancePage />} />

        

      </Routes>

      <FootNote />

    </Router>
  );
}

// export the app
export default App;

// buyer/seller terminology is now consistent - 'user' replaced with 'buyer' throughout
