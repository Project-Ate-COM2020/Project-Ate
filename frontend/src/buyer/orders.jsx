//order page 

import NavBar from "../reusableComponents/navBar.jsx";
import Listings from "../reusableComponents/listings.jsx";
import Reservations from "../bundlesComponents/bundles.jsx";

export default function Orders() {
    return (
      <>
        <NavBar />
        <Reservations includedAttributes = {["more info button", "pickup time"]} numberOfBundles = {50}/>
      </>
    );
  }

