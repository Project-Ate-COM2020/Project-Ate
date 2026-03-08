/* --- File Description --- */
/* This file will provide a reusable way to show multiple bundles, this 
will be useful in pages like the marketplace page for buyers and sellers

the following parameters will be passed:
 - number of bundles loaded 
 - various filter parameters (by seller, location, buyer)

There will probs be more I need to pass */

/* --- Current Issues --- */

/* Same problem with API */

/* --- Import Statements --- */
import NavBar from "../reusableComponents/navBar.jsx"

/* --- Test Data Declarations --- */
const bundleName = "Big Cheese Bundle";
const bundleCategory = "Dairy";
const imgPath = "/../../Dairy.jpg";
const pickupTime = "11:00 - 12:00";
const seller = "Cheesy Goods Incorporated";
const buyer = "Bobby";
const collectionCode = "QWERTY";
const price = 14.50;
const location = "Exeter";

/* --- Helper Functions  --- */
function SingleBundle({includedAttributes}) {

    let pickupTimeDisplayed;
    let bundleCategoryDisplayed;
    let sellerDisplayed;
    let buyerDisplayed;
    let collectionCodeDisplayed;
    let priceDisplayed;
    let locationDisplayed;
    let markCollectedButtonDisplayed;
    let unreserveBundleButton;

    for (const i of includedAttributes) {
        if (i == "pickup time") {pickupTimeDisplayed = true;}
        if (i == "bundle category") {bundleCategoryDisplayed = true;}
        if (i == "seller") {sellerDisplayed = true;}
        if (i == "buyer") {buyerDisplayed = true;}
        if (i == "collection code") {collectionCodeDisplayed = true;}
        if (i == "price") {priceDisplayed = true;}
        if (i == "location") {locationDisplayed = true;}
        if (i == "mark collected button") {markCollectedButtonDisplayed = true;}
        if (i == "unreserve bundle button") {unreserveBundleButton = true;}
    }

    return (
        <div className = "bundleContainer">
            <img src = {imgPath} />

            <h3>{bundleName}</h3>

            {pickupTimeDisplayed && <p>pickup time: {pickupTime}</p>}

            {bundleCategoryDisplayed && <p>Bundle Category: {bundleCategory}</p>}

            {sellerDisplayed && <p>Seller: {seller}</p>}

            {buyerDisplayed && <p>Buyer: {buyer}</p>}

            {collectionCodeDisplayed && <p>Collection Code: {collectionCode}</p>}

            {priceDisplayed && <p>Price: £{price}</p>}

            {locationDisplayed && <p>Location: {location}</p>}

            {markCollectedButtonDisplayed && <button>Mark Bundle as collected</button>}

            {unreserveBundleButton && <button>Unreserve bundle</button>}

        </div>
    )
}

/* --- Main Page Function --- */
function Bundles({includedAttributes=[]}) {
    return (
        <div className = "bundlesContainer">
            <NavBar />
            <SingleBundle includedAttributes/>

        </div>
    )
}

export default Bundles;