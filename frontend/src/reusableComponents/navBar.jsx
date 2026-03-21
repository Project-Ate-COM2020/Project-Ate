/* The nav bar goes at the top of the page to help navigate the website
add in the links to the different webpages needed and badges*/

import "./navBar.css";
import { NavLink } from "react-router-dom";


// Adding new user type - this method will be updated to using the user_type cookie when auth is finished
export default function NavBar() {
  const user_type = localStorage.getItem("user_type");
  if (user_type === "seller") {
    return (
      <nav>
      {/* use NavLink instead of <a href> so react router handles navigation (no page reload) */}
      <NavLink to="/seller/profile">Project-Ate</NavLink>
      <ul>
        <li><NavLink to="/seller/home">Home</NavLink></li>
        <li><NavLink to="/seller/analytics">Analytics</NavLink></li>
        <li><NavLink to="/seller/reservations">Reservations</NavLink></li>
        <li><NavLink to="/seller/postings">Postings</NavLink></li>
        <li><NavLink to="/seller/issues">Issues</NavLink></li>
      </ul>
    </nav>
    )
  } if (user_type === "buyer") {
    return (
    <nav>
      <NavLink to="/buyer/profile">Project-Ate</NavLink>
      <ul>
        <li><NavLink to="/buyer/game">Game</NavLink></li>
        <li><NavLink to="/buyer/home">Home</NavLink></li>
        <li><NavLink to="/buyer/orders">Orders</NavLink></li>
        <li><NavLink to="/buyer/report-issue">Report Issue</NavLink></li>
      </ul>
    </nav>
  );
  } else {
    return (
      <nav>
      <NavLink to="/buyer/home">Project-Ate</NavLink>
      <ul>
        <li><NavLink to="/login">Login</NavLink></li>
      </ul>
    </nav>
    );
  
}
}
