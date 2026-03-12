// for testing you need to reset the locat storage on the website using this localStorage.removeItem("cookie_consent_choice_v1") 



import { useEffect, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { sendCookieConsent } from "../api-legacy/cookieConsentApi";
import "./cookiesConsentStyle.css";

const CONSENT_KEY = "cookie_consent_choice_v1";

export default function CookiesConsent() {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const savedChoice = localStorage.getItem(CONSENT_KEY);
    const path = location.pathname;

    const isHome = path === "/";
    const isLogin = path === "/login";

    if ((isHome && !savedChoice) || (isLogin && savedChoice !== "accepted")) {
      setIsOpen(true);
      document.body.style.overflow = "hidden";
    } else {
      setIsOpen(false);
      document.body.style.overflow = "";
    }

    return () => {
      document.body.style.overflow = "";
    };
  }, [location.pathname]);

  const handleChoice = async (choice) => {
    localStorage.setItem(CONSENT_KEY, choice);
    

    try {
      await sendCookieConsent(choice);
    } catch (err) {
      console.error("Consent logging failed:", err);
    }

    setIsOpen(false);
    document.body.style.overflow = "";
  };

  if (!isOpen) return null;

  return (
    <div className="cookie-wrapper">
      <div className="cookie-overlay"></div>

      <div
        className="cookie-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="cookie-title"
        aria-describedby="cookie-description"
      >
        <div className="cookie-accent"></div>

        <h2 id="cookie-title" className="cookie-title">
          Cookies & Privacy
        </h2>

        <p id="cookie-description" className="cookie-text">
          We use essential cookies to keep Project-Ate secure and working
          correctly. Optional cookies help improve the platform and understand
          how people use the service.
        </p>

        <p className="cookie-text small">
          Read our{" "}
          <Link to="/terms-and-conditions" className="cookie-link">
            Terms & Conditions
          </Link>{" "}
          and{" "}
          <Link to="/cookie-policy" className="cookie-link">
            Cookie Policy
          </Link>
          .
        </p>

        <div className="cookie-buttons">
          <button
            type="button"
            className="cookie-btn secondary"
            onClick={() => handleChoice("rejected")}
          >
            Reject optional cookies
          </button>

          <button
            type="button"
            className="cookie-btn primary"
            onClick={() => handleChoice("accepted")}
          >
            Accept optional cookies
          </button>
        </div>
      </div>
    </div>
  );
}