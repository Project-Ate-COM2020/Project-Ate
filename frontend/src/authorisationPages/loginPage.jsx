/* Login needs to be changed to allow for seperate login for buyers and sellers */

// jsx for the central login page
import React, {useState} from "react";
import { useNavigate, Link } from "react-router-dom";
import { login, fetchMe } from "../api-legacy/authorisation";
import AuthLayout from "../reusableComponents/authLayout";
import { postData } from "../reusableComponents/api";

export default function LoginPage() {
  const navigate = useNavigate();

  // create state variables for form inputs
  const [accountType, setAccountType] = useState("buyer");
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");

  // UI feedback state ( loading + error )
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const credentials = await postData("auth/token", {"username" : identifier, "password" : password});

    localStorage.setItem("access_token", credentials.access);
    localStorage.setItem("refresh_token", credentials.refresh);

    console.log(credentials);

    const verify = await postData("auth/verify", {"token" : credentials.access});

    console.log(verify);

    if (accountType == "seller") {
      navigate("/seller");
    } if (accountType == "buyer") {
      navigate("/user");
    };

  };

  return (
    <AuthLayout title="Log in">
      {/* Error feedback */}
      {error && <div className="auth-error">{error}</div>}

      <form onSubmit={handleSubmit} className="auth-form">

        <label className="auth-label">
          Account Type
          <div>
            <label>
              <input
                type="radio"
                name="accountType"
                value="buyer"
                checked={accountType === "buyer"}
                onChange={(e) => setAccountType(e.target.value)}
              />
              Buyer
            </label>
            <label>
              <input
                type="radio"
                name="accountType"
                value="seller"
                checked={accountType === "seller"}
                onChange={(e) => setAccountType(e.target.value)}
              />
              Seller
            </label>
          </div>
        </label>

        
        <label className="auth-label">
          Username
          <input
            className="auth-input"
            value={identifier}
            onChange={(e) => setIdentifier(e.target.value)}
            placeholder="e.g. WillBrown@example.com"
            autoComplete="username"
            required
          />
        </label>

        <label className="auth-label">
          Password
          <input
            className="auth-input"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Your password"
            autoComplete="current-password"
            required
          />
        </label>

        {/* disable button while request is ongoing */}
        <button className="auth-primaryBtn" disabled={isLoading}>
          {isLoading ? "Logging in..." : "Log in"}
        </button>
      </form>

      <div className="auth-divider" />

      {/* sign up options, for buyer and seller */}
      <div className="auth-links">
        <span>New here?</span>
        <div className="auth-row">
          <Link to="/signup/buyer" className="auth-linkBtn">
            Buyer sign up
          </Link>
          <Link to="/signup/seller" className="auth-linkBtn">
            Seller sign up
          </Link>
        </div>
      </div>
    </AuthLayout>
  );
}
