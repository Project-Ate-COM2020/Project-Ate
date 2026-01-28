import { React } from  "react"
import NavBar from "../reusableComponents/navBar.jsx";
import sellerListings from "../reusableComponents/sellerListings.jsx";

// WE NEED TO EDIT THE LISTINGS FUNCTION TO ALLOW FOR SPEC

function SellerMarketplace(){
    return(
        <div>
            <NavBar />
            <h1>Seller Marketplace Page</h1>
            <p>Welcome to the Seller Marketplace! Here you can manage your listings and view your sales performance.</p>
            <sellerListings />
        </div>
    );
}

export default SellerMarketplace;