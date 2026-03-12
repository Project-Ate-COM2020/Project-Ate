import { useNavigate } from "react-router-dom";
import "./CookiePolicy.css";

export default function CookiePolicy() {
  const navigate = useNavigate();

  return (
    <main className="legal-page">

      <button
        className="legal-close"
        onClick={() => navigate(-1)}
        aria-label="Close"
      >
        ✕
      </button>

      <h1>Cookie Policy</h1>

      <p>
        This website uses cookies to provide essential functionality and,
        where consent is given, to improve performance and understand how the
        platform is used.
      </p>

      <h2>Essential Cookies</h2>
      <p>
        Essential cookies are required for security, login sessions, and basic
        functionality. These cookies cannot be disabled.
      </p>

      <h2>Optional Cookies</h2>
      <p>
        Optional cookies may include analytics or performance cookies used to
        understand how users interact with the platform. These cookies are only
        enabled if you choose to accept them.
      </p>

      <h2>Managing Cookie Preferences</h2>
      <p>
        You can change your cookie preferences at any time by adjusting your
        browser settings or by updating your cookie preferences within the
        website.
      </p>

    </main>
  );
}