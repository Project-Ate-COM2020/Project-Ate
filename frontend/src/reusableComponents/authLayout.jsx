// Import shared nav bar
import NavBar from "./navBar";
import "./auth.css";

// wrapper used for login/register pages
export default function authLayout({ title, children }) {
  return (
    <div className="auth-page">
      <NavBar />
      <div className="auth-container">
        <div className="auth-card">
          <h1 className="auth-brand">Project-Ate</h1>
          {/* page title (login / login) */}
          <p className="auth-title">{title}</p>
          {/* form content goes here*/}
          {children}
        </div>
      </div>
    </div>
  );
}
