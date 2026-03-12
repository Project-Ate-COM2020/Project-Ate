import { useNavigate } from "react-router-dom";
import "./TermsAndConditions.css";

export default function TermsAndConditions() {
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

      <h1>Terms and Conditions</h1>

      <p>
        These Terms and Conditions govern the use of the Project-Ate website.
        By using this platform, you agree to follow these terms.
      </p>

      <h2>1. Use of the Website</h2>
      <p>
        You agree to use the platform responsibly and lawfully. You must not use
        the website in any way that could harm the service or interfere with
        other users.
      </p>

      <h2>2. User Accounts</h2>
      <p>
        If you create an account, you are responsible for maintaining the
        confidentiality of your login credentials and any activity that occurs
        under your account.
      </p>

      <h2>3. Privacy and Cookies</h2>
      <p>
        Project-Ate uses essential cookies required for the operation and
        security of the platform. Optional cookies may be used to improve
        performance and analyse usage.
      </p>

      <h2>4. Intellectual Property</h2>
      <p>
        All content, branding, and design associated with this platform are the
        intellectual property of Project-Ate unless otherwise stated.
      </p>

      <h2>5. Service Availability</h2>
      <p>
        We aim to keep the platform available at all times but cannot guarantee
        uninterrupted service. Maintenance or updates may require temporary
        downtime.
      </p>

      <h2>6. Contact</h2>
      <p>
        If you have any questions about these Terms and Conditions, please
        contact the Project-Ate team.
      </p>

    </main>
  );
}