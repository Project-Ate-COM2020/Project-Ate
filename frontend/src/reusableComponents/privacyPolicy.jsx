import { useNavigate } from "react-router-dom";
import "../reusableComponents/legalPage.css";

export default function PrivacyPolicy() {

  const navigate = useNavigate();

  return (
    <div className="legal-page">

      <div className="legal-container">

        <button
          className="legal-close"
          onClick={() => navigate(-1)}
          aria-label="Close"
        >
          ×
        </button>

        <h1 className="legal-title">Privacy Policy</h1>

        <p className="legal-intro">
          This Privacy Policy explains how Project-Ate collects, uses and protects
          information when you use our platform.
        </p>

        <section className="legal-section">
          <h2>Information We Collect</h2>
          <p>
            We may collect account information, login details and platform
            usage data in order to operate the service and improve functionality.
          </p>
        </section>

      </div>

    </div>
  );
}