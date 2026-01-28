import { React } from  "react"
import NavBar from "../reusableComponents/navBar.jsx";
import SellerListings from "../reusableComponents/sellerListings.jsx";

// WE NEED TO EDIT THE LISTINGS FUNCTION TO ALLOW FOR INTEGRATION BETWEEN SELLER AND BUYER MARKETPLACE PAGES

// WE ALSO NEED TO FIND A WAY TO DEFINE 'currentsellerID' FROM LOGIN SESSION DATA

function SellerMarketplace(){
    return(
        <div>
        <div>
            <NavBar />
            <h1>Seller Marketplace Page</h1>
        </div>
        <div>
            <hr />
            <h2>Currently active listings: </h2>
            <SellerListings seller="currentSellerId" /> 

        </div>
        </div>
    );
}

export default SellerMarketplace;