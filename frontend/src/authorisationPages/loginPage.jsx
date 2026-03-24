/* --- File Description --- */

/* This file will allow for the login of a user, type is defined on the frontend and 
passed to the backend - simple single form submission */

/* --- Current Issues and Problems --- */

/* Main problem is there is no way to ensure the user picks the right account to login to - so error handling needs to be 
improved to allow proper redirecting*/

/* I also don't want to edit Harry's layout but it should be at some point */

/* --- Import Statements --- */
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import AuthLayout from "../reusableComponents/authLayout";
import { postData } from "../reusableComponents/api";

/* --- Main Page Functions --- */
export default function LoginPage() {
  const navigate = useNavigate();

  // create state variables for form inputs
  const [accountType, setAccountType] = useState("buyer");
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  

  // UI feedback state ( loading + error )
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const getUserTypeFromAccessToken = (accessToken, selectedType) => {
    try {
      const payload = jwtDecode(accessToken);
      const hasBuyer = !!payload.consumer_id;
      const hasSeller = !!payload.seller_id;
      const hasMaintainer = !!payload.maintainer_id;

      if (selectedType === "buyer" && hasBuyer) return "buyer";
      if (selectedType === "seller" && hasSeller) return "seller";
      if (selectedType === "maintainer" && hasMaintainer) return "maintainer";

      if (hasBuyer) return "buyer";
      if (hasSeller) return "seller";
      if (hasMaintainer) return "maintainer";
    } catch {
      return selectedType;
    }

    return selectedType;
  };

  const redirectPathForType = (type) => {
    if (type === "seller") return "/seller/home";
    if (type === "buyer") return "/buyer/home";
    if (type === "maintainer") return "/maintenance";
    return "/login";
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      const credentials = await postData("auth/token", {"username" : identifier, "password" : password}, false);

      if (!credentials || !credentials.access) {
        setError("Invalid username or password.");
        return;
      }

      localStorage.setItem("access_token", credentials.access);
      localStorage.setItem("refresh_token", credentials.refresh || "");
      const resolvedUserType = getUserTypeFromAccessToken(credentials.access, accountType);
      localStorage.setItem("user_type", resolvedUserType);

      navigate(redirectPathForType(resolvedUserType), { replace: true });
    } catch {
      setError("Could not log in. Please try again.");
    } finally {
      setIsLoading(false);
    }
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
            <label>
              <input
                type="radio"
                name="accountType"
                value="maintainer"
                checked={accountType === "maintainer"}
                onChange={(e) => setAccountType(e.target.value)}
              />
              Maintenence
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