// jsx for the central login page
import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { login, fetchMe } from "../api/authorisation";

export default function LoginPage() {
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
      // authenticate user
      await login({ identifier, password });
      // fetch profile info to decide if buyer or seller 
      try {
        const me = await fetchMe();

        // support backend role shapes
        const role =
          me?.role || me?.user_type || me?.account_type || me?.is_seller;

        if (role === "seller") {
          navigate("/seller");
        } else {
          navigate("/user");
        }
      } catch {
        // If profile fetch fails, default to user
        navigate("/user");
      }
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

    <div style={styles.page}>
      <div style={styles.card}>
        <h1 style={styles.title}>Project-Ate</h1>
        <p style={styles.subtitle}>Log in</p>

        {/* Error feedback */}
        {error && <div style={styles.error}>{error}</div>}

        <form onSubmit={handleSubmit} style={styles.form}>
          <label style={styles.label}>
            Email / Username
            <input
              style={styles.input}
              value={identifier}
              onChange={(e) => setIdentifier(e.target.value)}
              placeholder="e.g. WillBrown@example.com"
              autoComplete="username"
              required
            />
          </label>
          <label style={styles.label}>
            Password
            <input
              style={styles.input}
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Your password"
              autoComplete="current-password"
              required
            />
          </label>
          {/* disable button while request is ongoing */}
          <button style={styles.primaryBtn} disabled={isLoading}>
            {isLoading ? "Logging in..." : "Log in"}
          </button>
        </form>

        <div style={styles.divider} />

        {/* sign up options, for buyer and seller */}
        <div style={styles.links}>
          <span>New here?</span>
          <div style={styles.signupRow}>
            <Link to="/signup/buyer" style={styles.linkBtn}>
              Buyer sign up
            </Link>
            <Link to="/signup/seller" style={styles.linkBtn}>
              Seller sign up
            </Link>

          </div>
        </div>
      </div>
    </div>

  );
}

const styles = {
  page: {
    minHeight: "100vh",
    display: "grid",
    placeItems: "center",
    padding: 20,
    background: "#f6f7f9",
    fontFamily:  "system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Arial, sans-serif",
  },

  card: {
    width: "100%",
    maxWidth: 400,
    background: "white",
    border: "1px solid #e6e8ee",
    borderRadius: 12,
    padding: 20,
  },
  
  title: {
    margin: 0,
    fontSize: 24,
    user_select: "none",
    cursor: "default",
  },
  
  subtitle: {
    marginTop: 10,
    marginBottom: 16,
    color: "#555",
  },

  error: {
    background: "#ffe8e8",
    border: "1px solid #ffb3b3",
    padding: 10,
    borderRadius: 10,
    marginBottom: 12,
    color: "#7a0000",
    fontSize: 14,
  },

  form: {
    display: "grid",
    gap: 12,
  },

  label: {
    display: "grid",
    gap: 6,
    fontSize: 14,
  },

  input: {
    padding: "10px 12px",
    borderRadius: 8,
    border: "1px solid #cfd6e4",
    outline: "none",
    fontSize: 14, 
  },

  primaryBtn: {
    padding: "10px 12px",
    borderRadius: 8,
    border: "none",
    cursor: "pointer",
    fontSize: 14,
  },

  divider: {
    height: 1,
    background: "#eef0f5",
    margin: "16px 0",
  },

  links: {
    display: "grid",
    gap: 8,
    fontSize: 14,
  },

  signupRow: {
    display: "flex",
    gap: 10,
    flexWrap: "wrap",
  },
  
  linkBtn: {
    display: "inline-block",
    padding: "8px 10px",
    borderRadius: 8,
    border: "1px solid #cfd6e4",
    textDecoration: "none",
    color: "black",
    fontSize: 14,
  },
};
