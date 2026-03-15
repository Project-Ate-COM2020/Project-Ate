// jsx for the buyer sign up page (matches LoginPage styling)

// TODOS : error handling and tidying up this file

import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { signupBuyer } from "../api-legacy/authorisation";
import AuthLayout from "../reusableComponents/authLayout";
import { postData } from "../reusableComponents/api.jsx"

function BuyerSignupPage() {
  const navigate = useNavigate();

  // create state variables for form inputs
  const [displayName, setDisplayName] = useState("");
  const [email, setEmail] = useState("");
  const [password1, setPassword1] = useState("");
  const [password2, setPassword2] = useState("");
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

    // basic password checks ( backend will do futher validation )
    if (password1 !== password2) {
      setError("Passwords do not match");
      return;
    }
    if (password1.length < 8) {
      setError("Password must be at least 8 characters");
      return;
    }

    const dataToPost = {
      "email" : email,
      "password" : password2,
      "username": displayName,
      "first_name": firstName,
      "last_name" : lastName,
    }

    const response = postData("auth/user", dataToPost, false);
    
    // Testing purposes
    console.log(response);

  };

  return (
    <AuthLayout title="Buyer sign up">
      {/* Error or success feedback */}
      {error && <div className="auth-error">{error}</div>}
      {success && <div className="auth-success">{success}</div>}

      <form onSubmit={handleSubmit} className="auth-form">
        <label className="auth-label">
          Username
          <input
            className="auth-input"
            value={displayName}
            onChange={(e) => setDisplayName(e.target.value)}
            placeholder="e.g. WillB123"
            autoComplete="name"
            required
          />
        </label>

        <label className="auth-label">
          First Name
          <input
            className="auth-input"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
            placeholder="e.g. Will"
            autoComplete="name"
            required
          />
        </label>

        <label className="auth-label">
          Last Name
          <input
            className="auth-input"
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
            placeholder="e.g. Brown"
            autoComplete="name"
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
            placeholder="e.g. WillBrown@example.com"
            autoComplete="email"
            required
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
          {isLoading ? "Creating account..." : "Create account"}
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
export default BuyerSignupPage;