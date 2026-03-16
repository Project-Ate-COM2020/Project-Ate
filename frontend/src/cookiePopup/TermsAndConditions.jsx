import { useNavigate } from "react-router-dom";
import "../reusableComponents/legalPage.css";

export default function TermsAndConditions() {

  const navigate = useNavigate();

  return (
    <main className="legal-page">

      <div className="legal-container">

        <button
          className="legal-close"
          onClick={() => navigate(-1)}
          aria-label="Close"
        >
          ✕
        </button>

        <h1 className="legal-title">Terms and Conditions</h1>

        <p className="legal-intro">
          These Terms and Conditions govern the use of the Project-Ate platform.
          By accessing or using this website, you agree to comply with these
          terms.
        </p>

        <section className="legal-section">
          <h2>1. Use of the Platform</h2>
          <p>
            Users must use the platform responsibly and lawfully. You must not
            use the website in any way that could damage the platform or
            interfere with other users.
          </p>
        </section>

        <section className="legal-section">
          <h2>2. User Accounts</h2>
          <p>
            If you create an account, you are responsible for maintaining the
            confidentiality of your login credentials and all activity under
            your account.
          </p>
        </section>

        <section className="legal-section">
          <h2>3. Acceptable Use</h2>
          <p>
            Users must not attempt to misuse the platform, access unauthorised
            areas, or introduce malicious software.
          </p>
        </section>

        <section className="legal-section">
          <h2>4. Privacy and Cookies</h2>
          <p>
            Project-Ate uses essential cookies required for the operation and
            security of the platform. Optional cookies may be used to improve
            performance and analyse usage.
          </p>
        </section>

        <section className="legal-section">
          <h2>5. Intellectual Property</h2>
          <p>
            All content, branding, and design associated with this platform are
            the intellectual property of Project-Ate unless otherwise stated.
          </p>
        </section>

        <section className="legal-section">
          <h2>6. Service Availability</h2>
          <p>
            We aim to keep the platform available but cannot guarantee
            uninterrupted service. Maintenance or updates may require temporary
            downtime.
          </p>
        </section>

        <section className="legal-section">
          <h2>7. Limitation of Liability</h2>
          <p>
            Project-Ate will not be liable for losses arising from use of the
            platform to the fullest extent permitted by law.
          </p>
        </section>

        <section className="legal-section">
          <h2>8. Changes to These Terms</h2>
          <p>
            These Terms and Conditions may be updated periodically. Continued
            use of the platform indicates acceptance of the updated terms.
          </p>
        </section>

        <section className="legal-section">
          <h2>9. Governing Law</h2>
          <p>
            These terms are governed by the laws of the United Kingdom.
          </p>
        </section>

        <section className="legal-section">
          <h2>10. Contact</h2>
          <p>
            If you have questions about these Terms and Conditions, please
            contact the Project-Ate team.
          </p>
        </section>

      </div>

    </main>
  );
}