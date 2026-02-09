// jsx for the seller sign up page ( matches LoginPage + BuyerSignupPage styling )
import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { signupSeller } from "../api/authorisation";

export default function SellerSignupPage() {
  const navigate = useNavigate();

  // create state variables for form inputs
  const [businessName, setBusinessName] = useState("");
  const [email, setEmail] = useState("");
  const [password1, setPassword1] = useState("");
  const [password2, setPassword2] = useState("");

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

    setIsLoading(true);

    try {
      // create seller account
      await signupSeller({
        email,
        password: password1,
        businessName,
      });

      setSuccess("Seller account successfully created. You can now log in.");
      navigate("/login");
    } catch (err) {
      // make error messages user friendly
      console.error(err);
      let message = "Unable to sign up. Please try again.";

      // handle network errors
      if (err?.message === "Failed to fetch") {
        message =
          "Unable to connect to the server, please check your internet connection";
      }

      // requestJson throws Error(...) with message
      if (typeof err?.message === "string" && err.message.trim()) {
        message = err.message;
      }

      setError(message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <h1 style={styles.title}>Project-Ate</h1>
        <p style={styles.subtitle}>Seller sign up</p>

        {/* Error or success feedback */}
        {error && <div style={styles.error}>{error}</div>}
        {success && <div style={styles.success}>{success}</div>}

        <form onSubmit={handleSubmit} style={styles.form}>
          <label style={styles.label}>
            Business name
            <input
              style={styles.input}
              value={businessName}
              onChange={(e) => setBusinessName(e.target.value)}
              placeholder="e.g. Green Street Bakery"
              autoComplete="organization"
              required
            />
          </label>

          <label style={styles.label}>
            Email
            <input
              style={styles.input}
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="e.g. bakery@example.com"
              autoComplete="email"
              required
            />
          </label>

          <label style={styles.label}>
            Password
            <input
              style={styles.input}
              type="password"
              value={password1}
              onChange={(e) => setPassword1(e.target.value)}
              placeholder="Create a password"
              autoComplete="new-password"
              required
            />
          </label>

          <label style={styles.label}>
            Confirm password
            <input
              style={styles.input}
              type="password"
              value={password2}
              onChange={(e) => setPassword2(e.target.value)}
              placeholder="Re-enter your password"
              autoComplete="new-password"
              required
            />
          </label>

          {/* disable button while request is ongoing */}
          <button style={styles.primaryBtn} disabled={isLoading}>
            {isLoading ? "Creating account..." : "Create seller account"}
          </button>
        </form>

        <div style={styles.divider} />

        <div style={styles.links}>
          <span>Already have an account?</span>
          <div style={styles.signupRow}>
            <Link to="/login" style={styles.linkBtn}>
              Back to login
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

// same base as login + buyer signup page
const styles = {

  page: {
    minHeight: "100vh",
    display: "grid",
    placeItems: "center",
    padding: 20,
    background: "#f6f7f9",
    fontFamily:
      "system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Arial, sans-serif",
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
    userSelect: "none",
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

  success: {
    background: "#e9ffe8",
    border: "1px solid #b6f0b3",
    padding: 10,
    borderRadius: 10,
    marginBottom: 12,
    color: "#0b5f00",
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
