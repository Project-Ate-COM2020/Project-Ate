import { Link } from "react-router-dom";
import "./footNote.css";

export default function FootNote() {
  return (
    <footer className="site-footnote">

      <div className="footnote-links">
        <Link to="/terms-and-conditions">Terms & Conditions</Link>
        <Link to="/cookie-policy">Cookie Policy</Link>
        <Link to="/privacy-policy">Privacy Policy</Link>
      </div>

      <div className="footnote-bottom">
        <p>© {new Date().getFullYear()} Project-Ate. All rights reserved.</p>
      </div>

    </footer>
  );
}