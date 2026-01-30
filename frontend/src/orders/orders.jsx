//order page 

import NavBar from "../reusableComponents/navBar.jsx";
import Listings from "../reusableComponents/listings.jsx";

export default function Orders() {
    return (
      <>
        <NavBar />
        <Listings mode="orders" />
      </>
    );
  }

