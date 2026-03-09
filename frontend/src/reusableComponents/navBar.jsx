/* The nav bar goes at the top of the page to help navigate the website
add in the links to the different webpages needed and badges*/

import "./navBar.css";
import { NavLink } from "react-router-dom";


// Adding new user type - this method will be updated to using the user_type cookie when auth is finished
export default function NavBar( {user_type} ) {
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
      </ul>
    </nav>
    )
  } else {
  return (
    <nav>
      {/* use NavLink instead of <a href> so react router handles navigation (no page reload) */}
      <NavLink to="/user">Project-Ate</NavLink>
      <ul>
        <li><NavLink to="/game">Game</NavLink></li>
        <li><NavLink to="/buyer-profile">Profile</NavLink></li>
        {/* <li><NavLink to="/basket">Basket</NavLink></li> */}
        <li><NavLink to="/login">Login</NavLink></li>
        <li><NavLink to="/orders">Orders</NavLink></li>
      </ul>
    </nav>
  );
}
}
