/* --- General Import Statements --- */
import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";


// import the files for each URL endpoint
import Orders from "./buyer/orders.jsx";
import LoginPage from "./authorisationPages/loginPage.jsx";
import GamePage from "./buyer/game.jsx";
import MarketplacePage from "./buyer/marketplace.jsx";
import PageNotFound from "./reusableComponents/pageNotFound.jsx";
import UserHomePage from "./homePage/userHomePage.jsx";
import HomePage from "./homePage/HomePage.jsx";
//import Basket from "./Basket/basket.jsx";

/* --- Auth Imports --- */
import SellerSignupPage from "./authorisationPages/sellerSignupPage.jsx";
import BuyerSignupPage from "./authorisationPages/buyerSignupPage.jsx";

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
import BuyerProfilePage from "./buyer/BuyerProfilePage.jsx";
import IssueReportingPage from "./buyer/issueReportingPage.jsx";
import SellerIssuesPage from "./seller/sellerIssuesPage.jsx";

/* --- Webpage Imports --- */
import CookiesConsent from "./cookiePopup/cookiesConsent";
import TermsAndConditions from "./cookiePopup/TermsAndConditions";
import CookiePolicy from "./cookiePopup/CookiePolicy";
import FootNote from "./reusableComponents/footnote";
import PrivacyPolicy from "./reusableComponents/privacyPolicy";

/* --- Maintaner Imports ---*/
import MaintenancePage from "./maintenancePage/maintenancePage.jsx";

/* --- Route Guards --- */

// Redirects logged-in users away from guest-only pages (login, signup, landing)
function GuestOnlyRoute({ children }) {
  const token = localStorage.getItem("access_token");
  const userType = localStorage.getItem("user_type");
  if (token) {
    return <Navigate to={userType === "seller" ? "/seller/home" : "/buyer/home"} replace />;
  }
  return children;
}

// Requires authentication
function ProtectedRoute({ children, requiredType }) {
  const token = localStorage.getItem("access_token");
  const userType = localStorage.getItem("user_type");
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  if (requiredType && userType !== requiredType) {
    return <Navigate to={userType === "seller" ? "/seller/home" : "/buyer/home"} replace />;
  }
  return children;
}

// simple function defining the element to be returned based on the URL
function App() {
  return (
    <Router>

      <CookiesConsent />

      <Routes>
        {/* Guest-only paths — redirect logged-in users to their home */}
        <Route path="/" element={<GuestOnlyRoute><HomePage /></GuestOnlyRoute>} />
        <Route path="/login" element={<GuestOnlyRoute><LoginPage /></GuestOnlyRoute>} />
        <Route path="/seller/login" element={<GuestOnlyRoute><LoginPage /></GuestOnlyRoute>} />
        <Route path="/signup/buyer" element={<GuestOnlyRoute><BuyerSignupPage /></GuestOnlyRoute>} />
        <Route path="/signup/seller" element={<GuestOnlyRoute><SellerSignupPage /></GuestOnlyRoute>} />

        {/* Buyer-only paths */}
        <Route path="/buyer/home" element={<ProtectedRoute requiredType="buyer"><UserHomePage /></ProtectedRoute>} />
        <Route path="/buyer/profile" element={<ProtectedRoute requiredType="buyer"><BuyerProfilePage /></ProtectedRoute>} />
        <Route path="/buyer/orders" element={<ProtectedRoute requiredType="buyer"><Orders /></ProtectedRoute>} />
        <Route path="/buyer/report-issue" element={<ProtectedRoute requiredType="buyer"><IssueReportingPage /></ProtectedRoute>} />
        <Route path="/game" element={<ProtectedRoute requiredType="buyer"><GamePage /></ProtectedRoute>} />
        <Route path="/buyer-profile" element={<ProtectedRoute requiredType="buyer"><BuyerProfilePage /></ProtectedRoute>} />
        {/*<Route path="/basket" element={<ProtectedRoute requiredType="buyer"><Basket /></ProtectedRoute>} />*/}

        {/* Seller-only paths */}
        <Route path="/seller/home" element={<ProtectedRoute requiredType="seller"><SellerHomePage /></ProtectedRoute>} />
        <Route path="/seller" element={<ProtectedRoute requiredType="seller"><SellerHomePage /></ProtectedRoute>} />
        <Route path="/seller/profile" element={<ProtectedRoute requiredType="seller"><SellerProfilePage /></ProtectedRoute>} />
        <Route path="/seller/createPosting" element={<ProtectedRoute requiredType="seller"><CreatePostPage /></ProtectedRoute>} />
        <Route path="/seller/reservation" element={<ProtectedRoute requiredType="seller"><Reservation /></ProtectedRoute>} />
        <Route path="/seller/reservations" element={<ProtectedRoute requiredType="seller"><Reservations /></ProtectedRoute>} />
        <Route path="/seller/posting" element={<ProtectedRoute requiredType="seller"><Posting /></ProtectedRoute>} />
        <Route path="/seller/postings" element={<ProtectedRoute requiredType="seller"><Postings /></ProtectedRoute>} />
        <Route path="/seller/analytics" element={<ProtectedRoute requiredType="seller"><Analytics /></ProtectedRoute>} />
        <Route path="/seller/issues" element={<ProtectedRoute requiredType="seller"><SellerIssuesPage /></ProtectedRoute>} />

        {/* Legal pages */}
        <Route path="/terms-and-conditions" element={<TermsAndConditions />} />
        <Route path="/cookie-policy" element={<CookiePolicy />} />
        <Route path="/privacy-policy" element={<PrivacyPolicy />} />

        {/* maintainer Page */}
        <Route path="/maintenance" element={<MaintenancePage />} />

        {/* Catch-all */}
        <Route path="/user" element={<Navigate to="/buyer/home" replace />} />
        <Route path="*" element={<PageNotFound />} />
      </Routes>

      <FootNote />

    </Router>
  );
}

// export the app
export default App;
