/* Updated as of 06/03/2026 by Jamie - needs significant work to make it take proper inputs and clean up the loop*/

// jsx for the seller sign up page ( matches LoginPage + BuyerSignupPage styling )
import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { signupSeller } from "../api-legacy/authorisation";
import AuthLayout from "../reusableComponents/authLayout";

export default function SellerSignupPage() {
  const navigate = useNavigate();

  // create state variables for form inputs
  const [businessName, setBusinessName] = useState("");
  const [email, setEmail] = useState("");
  const [password1, setPassword1] = useState("");
  const [password2, setPassword2] = useState("");
  const [location, setLocation] = useState("");
  const [openingHours, setOpeningHours] = useState("");
  

  // UI feedback state ( loading + error + success )
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  async function handleSubmit() {
    // Prevent default form submission
    event.preventDefault();
    setIsLoading(true);
    setError("");
    setSuccess("");

    // Basic validation
    if (password1 !== password2) {
      setError("Passwords do not match.");
      setIsLoading(false);
      return;
    }

    try {
      const response = await signupSeller({
        email,
        password: password1,
        sellerName: businessName,
        location,
        openingHours,
        
      });
      setSuccess("Seller account created successfully!");
      setIsLoading(false);
      // Optionally redirect or clear form
      // navigate("/login");
    } catch (err) {
      setError("Failed to create seller account.");
      setIsLoading(false);
    }
  }

  return (
    <AuthLayout title="Seller sign up">
      {/* Error or success feedback */}
      {error && <div className="auth-error">{error}</div>}
      {success && <div className="auth-success">{success}</div>}

      <form onSubmit={handleSubmit} className="auth-form">
        <label className="auth-label">
          Business name
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
