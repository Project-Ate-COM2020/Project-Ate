//order page 

import NavBar from "../reusableComponents/navBar.jsx";
import Listingsv2 from "../reusableComponents/listings-v2.jsx";

export default function Orders() {
    return (
      <>
        <NavBar />
        <Listingsv2 mode = "orders"/>
      </>
    );
  }

