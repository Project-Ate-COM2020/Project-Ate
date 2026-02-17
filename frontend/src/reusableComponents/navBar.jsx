/* The nav bar goes at the top of the page to help navigate the website
add in the links to the different webpages needed and badges*/

import "./navBar.css";
import { NavLink } from "react-router-dom";

export default function NavBar() {
  return (
    <nav>
      {/* use NavLink instead of <a href> so react router handles navigation (no page reload) */}
      <NavLink to="/user">Project-Ate</NavLink>
      <ul>
        <li><NavLink to="/game">Profile</NavLink></li>
        {/* <li><NavLink to="/basket">Basket</NavLink></li> */}
        <li><NavLink to="/login">Login</NavLink></li>
        <li><NavLink to="/orders">Orders</NavLink></li>
      </ul>
    </nav>
  );
}
