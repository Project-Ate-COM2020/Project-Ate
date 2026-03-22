/* Updated as of 06/03/2026 by Jamie - needs significant work to make it take proper inputs and clean up the loop*/

// jsx for the seller sign up page ( matches LoginPage + BuyerSignupPage styling )
import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import AuthLayout from "../reusableComponents/authLayout";
import {postData } from "../reusableComponents/api.jsx";

export default function SellerSignupPage() {
  const navigate = useNavigate();

  // create state variables for form inputs
  const [businessName, setBusinessName] = useState("");
  const [email, setEmail] = useState("");
  const [password1, setPassword1] = useState("");
  const [password2, setPassword2] = useState("");
  const [location, setLocation] = useState("");
  const [openingHours, setOpeningHours] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  
  

  // UI feedback state ( loading + error + success )
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setIsLoading(true);

    try {

    // basic password checks ( backend will do futher validation )
    if (password1 !== password2) {
      setError("Passwords do not match");
      setIsLoading(false);
      return;
    }
    if (password1.length < 8) {
      setError("Password must be at least 8 characters");
      setIsLoading(false);
      return;
    }

    const dataToPost = {
      "email" : email,
      "password" : password2,
      "username": businessName,
      "first_name": firstName,
      "last_name" : lastName,
    }

    const createdUser = await postData("auth/user", dataToPost, false);
    if (!createdUser || !createdUser.id) {
      setError("Could not create user account.");
      return;
    }
    
    // Testing purposes
    console.log(createdUser);

    const credentials = await postData("auth/token", {"password": password2, "username": businessName}, false);
    if (!credentials || !credentials.access) {
      setError("Account created, but automatic login failed. Please log in manually.");
      return;
    }

    // Testing purposes (POTENTIAL SECURITY RISK)
    console.log(credentials);

    const sellerData = {
      "display_name" : businessName,
      "user_id" : createdUser.id,
      "name": businessName,
      "location": location,
    }

    const createdSellerResponse = await fetch("http://localhost:8000/marketplace/seller", {
      method: "POST",
      headers: {
        "Authorization": "Bearer " + credentials.access,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(sellerData),
    });

    const createdSeller = await createdSellerResponse.json();
    if (!createdSellerResponse.ok || !createdSeller) {
      setError("Could not finish seller registration.");
      return;
    }

    // Testing Purposes
    console.log(createdSeller);

    localStorage.setItem("access_token", credentials.access);
    localStorage.setItem("refresh_token", credentials.refresh || "");
    localStorage.setItem("user_type", "seller");

    navigate("/seller/home");
    } catch {
      setError("Could not create account. Please try again.");
    } finally {
      setIsLoading(false);
    }
  
  };

  return (
    <AuthLayout title="Seller sign up">
      {/* Error or success feedback */}
      {error && <div className="auth-error">{error}</div>}
      {success && <div className="auth-success">{success}</div>}

      <form onSubmit={handleSubmit} className="auth-form">
        <label className="auth-label">
          Business Username
          <input
            className="auth-input"
            value={businessName}
            onChange={(e) => setBusinessName(e.target.value)}
            placeholder="e.g. Green Street Bakery"
            autoComplete="organization"
            required
          />
        </label>

        <label className="auth-label">
          Email
          <input
            className="auth-input"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="e.g. bakery@example.com"
            autoComplete="email"
            required
          />
        </label>

        <label className="auth-label">
          First Name
          <input
            className="auth-input"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
            placeholder="Will"
            autoComplete="email"
            required
          />
        </label>

        <label className="auth-label">
          Last Name
          <input
            className="auth-input"
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
            placeholder="Brown"
            autoComplete="email"
            required
          />
        </label>

        <label className="auth-label">
          Location (postcode)
          <input
            className="auth-input"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="e.g. SW1A 1AA"
            autoComplete="postal-code"
            required
          />
        </label>

        <label className="auth-label">
          Opening hours
          <input
            className="auth-input"
            value={openingHours}
            onChange={(e) => setOpeningHours(e.target.value)}
            placeholder="e.g. Mon-Fri 8am-6pm"
            autoComplete="off"
          />
        </label>

        

        <label className="auth-label">
          Password
          <input
            className="auth-input"
            type="password"
            value={password1}
            onChange={(e) => setPassword1(e.target.value)}
            placeholder="Create a password"
            autoComplete="new-password"
            required
          />
        </label>

        <label className="auth-label">
          Confirm password
          <input
            className="auth-input"
            type="password"
            value={password2}
            onChange={(e) => setPassword2(e.target.value)}
            placeholder="Re-enter your password"
            autoComplete="new-password"
            required
          />
        </label>

        {/* disable button while request is ongoing */}
        <button className="auth-primaryBtn" disabled={isLoading}>
          {isLoading ? "Creating account..." : "Create seller account"}
        </button>
      </form>
   

      <div className="auth-divider" />

      <div className="auth-links">
        <span>Already have an account?</span>
        <div className="auth-row">
          <Link to="/login" className="auth-linkBtn">
            Back to login
          </Link>
        </div>
      </div>
    </AuthLayout>
  );
}
