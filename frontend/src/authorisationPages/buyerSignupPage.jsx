/* --- File Description --- */

/* Buyer Sign up page - creates a buyer user and logs the client in as that user */

/* --- Problems and Issues --- */

/* Need to tidy up and make the page look nicer */

/* --- Import Statements --- */
import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import AuthLayout from "../reusableComponents/authLayout";
import { postData } from "../reusableComponents/api.jsx";

function BuyerSignupPage() {
  const navigate = useNavigate();

  // create state variables for form inputs
  const [displayName, setDisplayName] = useState("");
  const [username, setUsername] = useState("");
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
      "username": username,
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

    const credentials = await postData("auth/token", {"password": password2, "username": username}, false);
    if (!credentials || !credentials.access) {
      setError("Account created, but automatic login failed. Please log in manually.");
      return;
    }

    // Testing purposes (POTENTIAL SECURITY RISK)
    console.log(credentials);

    const buyerData = {
      "display_name" : displayName,
      "user_id" : createdUser.id,
    }

    const createdBuyerResponse = await fetch("http://localhost:8000/marketplace/consumer", {
      method: "POST",
      headers: {
        "Authorization": "Bearer " + credentials.access,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(buyerData),
    });

    const createdBuyer = await createdBuyerResponse.json();
    if (!createdBuyerResponse.ok || !createdBuyer) {
      setError("Could not finish buyer registration.");
      return;
    }

    // Testing Purposes
    console.log(createdBuyer);

    localStorage.setItem("access_token", credentials.access);
    localStorage.setItem("refresh_token", credentials.refresh || "");
    localStorage.setItem("user_type", "buyer");

    navigate("/buyer/home");
    } catch {
      setError("Could not create account. Please try again.");
    } finally {
      setIsLoading(false);
    }


  };

  return (
    <AuthLayout title="Buyer sign up">
      {/* Error or success feedback */}
      {error && <div className="auth-error">{error}</div>}
      {success && <div className="auth-success">{success}</div>}

      <form onSubmit={handleSubmit} className="auth-form">
        <label className="auth-label">
          Display Name
          <input
            className="auth-input"
            value={displayName}
            onChange={(e) => setDisplayName(e.target.value)}
            placeholder="e.g. Will Brown"
            autoComplete="name"
            required
          />
        </label>

        <label className="auth-label">
          Username
          <input
            className="auth-input"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
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