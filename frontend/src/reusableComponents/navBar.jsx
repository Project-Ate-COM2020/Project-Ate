/* The nav bar goes at the top of the page to help navigate the website
add in the links to the different webpages needed and badges*/

import "./navBar.css";
import { NavLink } from "react-router-dom";

function clearAuth() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("user_type");
}

export default function NavBar({ user_type }) {
  if (user_type === "seller") {
    return (
      <nav>
        <NavLink to="/seller/home">Project-Ate</NavLink>
        <ul>
          <li><NavLink to="/seller/analytics">Analytics</NavLink></li>
          <li><NavLink to="/seller/reservations">Reservations</NavLink></li>
          <li><NavLink to="/seller/postings">Postings</NavLink></li>
          <li><NavLink to="/seller/issues">Issues</NavLink></li>
          <li><NavLink to="/login" onClick={clearAuth}>Log out</NavLink></li>
        </ul>
      </nav>
    );
  } else {
    return (
      <nav>
        <NavLink to="/buyer/home">Project-Ate</NavLink>
        <ul>
          <li><NavLink to="/game">Game</NavLink></li>
          <li><NavLink to="/buyer/profile">Profile</NavLink></li>
          {/* <li><NavLink to="/basket">Basket</NavLink></li> */}
          <li><NavLink to="/buyer/orders">Orders</NavLink></li>
          <li><NavLink to="/buyer/report-issue">Report Issue</NavLink></li>
          <li><NavLink to="/login" onClick={clearAuth}>Log out</NavLink></li>
        </ul>
      </nav>
    );
  }
}
