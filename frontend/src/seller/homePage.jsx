/* --- File Description --- */
/* Also Following Will's Description to some extent, this file act more as a preview for the seller - allow some small actions to be made - and allow 
the seller to breakout into dedicated pages such as analytics and bundleCreation. 

Includes: 
 - Seller info
 - Analytics
 - Seller Bundle Postings
 - Seller Bundle Reservations
 - Seller Bundle Post Creation + Forecasting
 
each of these will be split up into helper functions for readability and maintainability
*/

/* --- Current Issues --- */

/* The main issue is the current backend bug preventing from loggin in - this means when the backend is fixed 
and endpoints refactored, the endpoints and maybe the parsing for this file will also need to change */

/* --- Import Statements --- */
import NavBar from "../reusableComponents/navBar.jsx";
import Postings from "../bundlesComponents/postings.jsx";
import ReservedBundles from "../bundlesComponents/bundles.jsx";

/* --- Test Data Declarations --- */
const sellerName = "Test Seller Name";
const location = "Test Seller location";

const numListings = 120;
const amountRevenue = 2400;
const percentageListingsCollected = 0.7;

let time_window;
let category;
let weather;
let day_of_week;
let no_bundles;

/* --- Helper Functions --- */

function SellerInfo() {
    return (
        <div className = "sellerInfo">
            <h4>Seller Info</h4>

            <div className = "infoContainer">
                
                <div className = "info">
                    <p>Name: {sellerName}</p>
                </div>

                <div className = "info">
                    <p>Location: {location}</p>
                </div>

            </div>
        </div>
    )
}

function Analytics() {
    return (
        <div className = "analytics">

            <h4>Analytics</h4>

            <div className = "infoContainer">

                <div className = "info">
                    <p>Total Number of Listings: {numListings}</p>
                </div>

                <div className = "info">
                    <p>Total Revenue: {amountRevenue}</p>
                </div>

                <div className = "info">
                    <p>Percentage of Listings Collected by Users: {percentageListingsCollected*100}%</p>
                </div>

            </div>
        </div>
    )
}

function BundlePostings() {


    return (
        <div>
            <h4>Bundle Postings</h4>
            <Postings includedAttributes = {["price", "more info button"]} />
        </div>
    )
}

function BundleReservations() {
    return (
        <div>
            <h4>Customer Reservations</h4>
            <ReservedBundles includedAttributes = {["buyer", "more info button"]} />
        </div>
    )
}

function BundlePostCreation() {
    return (
        <div className = "BundlePostCreation">
            
        </div>
    )
}

/* --- Main Page Function --- */

function SellerHomePage() {
    return (
        <div>
            <NavBar />
            <SellerInfo />
            <Analytics />
            <BundlePostings />
            <BundleReservations />
            <BundlePostCreation />
        </div>
    )

}

export default SellerHomePage;