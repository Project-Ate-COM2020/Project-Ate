/* Login needs to be changed to allow for seperate login for buyers and sellers */

// jsx for the central login page
import React, {useState} from "react";
import { useNavigate, Link } from "react-router-dom";
import { login, fetchMe } from "../api-legacy/authorisation";
import AuthLayout from "../reusableComponents/authLayout";
import useGetData from "../api/post";

export default function SellerLoginPage() {
  const navigate = useNavigate();

  // create state variables for form inputs
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");

  // UI feedback state ( loading + error )
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      the_post_data = {
        username : identifier,
        password : password
      }
      const { data, loading } = useGetData("marketplace/seller/auth/token", the_post_data, false);
      navigate("/seller");
    } catch (err) {
      // make error messages user friendly
      console.error(err);
      let message = "Incorrect username or password";

      // handle network errors
      if (err?.message === "Failed to fetch") {
        message =
          "Unable to connect to the server, please check your internet connection";
      }

      // check for http status codes
      if (err?.status === 401) message = "Incorrect username or password";
      if (err?.status === 403) message = "You're not authorised to log in";

      setError(message);
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
          Email / Username
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
