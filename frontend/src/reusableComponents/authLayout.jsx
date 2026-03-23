// Import shared nav bar
import { NavLink } from "react-router-dom";
import "./auth.css";

// wrapper used for login/register pages
export default function authLayout({ title, children }) {
  return (
    <div className="auth-page">
      <header className="auth-header">
        <NavLink to="/" className="auth-header-logo">Project-Ate</NavLink>
      </header>
      <div className="auth-container">

        {/* Green side with branding to match the home page */}
        <div className="auth-left">
          <h1 className="auth-left-logo">Project-Ate</h1>
          <p className="auth-left-tagline">Eat well, make a difference.</p>
          <p className="auth-left-sub">Fresh food bundles designed around your lifestyle — less waste, more taste.</p>
        </div>

        {/* White side with the form */}
        <div className="auth-right">
          <div className="auth-card">
            <h2 className="auth-brand">Welcome back!</h2>
            {children}
          </div>
        </div>

      </div>
    </div>
  );
}
