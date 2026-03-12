/* --- File Description --- */
/* This file will provide a reusable way to show a single bundle, 
these are individual bundles so will be implemented in the reservations page for buyers and sellers,
the component will have to take a number of parameters to ensure reusablity.

I will list the ones I can think of here:

 - Infor displayed in bundle

I am sure this list will expand as I code the libray and as it is implemented
*/

/* --- Current Issues --- */

/* The main issue is the current backend bug preventing from loggin in - this means when the backend is fixed 
and endpoints refactored, the endpoints and maybe the parsing for this file will also need to change */

/* This file will be idealistic only - no API access, however due to my API library it shouldn't be too 
hard to add once the backend is ready */

/* --- Import Statements --- */
import "./bundle.css";

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

/* --- Helper Functions --- */
function OptionalContainer( { includedAttributes } ) {

    let pickupTimeDisplayed;
    let bundleCategoryDisplayed;
    let sellerDisplayed;
    let buyerDisplayed;
    let collectionCodeDisplayed;
    let priceDisplayed;
    let locationDisplayed;
    let markCollectedButtonDisplayed;
    let unreserveBundleButtonDisplayed;

    for (const i of includedAttributes) {
        if (i == "pickup time") {pickupTimeDisplayed = true;}
        if (i == "bundle category") {bundleCategoryDisplayed = true;}
        if (i == "seller") {sellerDisplayed = true;}
        if (i == "buyer") {buyerDisplayed = true;}
        if (i == "collection code") {collectionCodeDisplayed = true;}
        if (i == "price") {priceDisplayed = true;}
        if (i == "location") {locationDisplayed = true;}
        if (i == "mark collected button") {markCollectedButtonDisplayed = true;}
        if (i == "unreserve bundle button") {unreserveBundleButtonDisplayed = true;}
    }

    return (
        <div className = "infoContainer">
            {pickupTimeDisplayed && <p>pickup time: {pickupTime}</p>}

            {bundleCategoryDisplayed && <p>Bundle Category: {bundleCategory}</p>}

            {sellerDisplayed && <p>Seller: {seller}</p>}

            {buyerDisplayed && <p>Buyer: {buyer}</p>}

            {collectionCodeDisplayed && <p>Collection Code: {collectionCode}</p>}

            {priceDisplayed && <p>Price: £{price}</p>}

            {locationDisplayed && <p>Location: {location}</p>}

            {markCollectedButtonDisplayed && <button>Mark Bundle as collected</button>}

            {unreserveBundleButtonDisplayed && <button>Unreserve bundle</button>}

            
        </div>
    )
}

/* --- Main Function --- */
function Bundle( {includedAttributes = [], backfunction} ) {

    return (
        <div className = "bundleDisplay">
            <button onClick={backfunction}>X</button>
            <div className = "bundleTitle">
                <h3>{bundleName}</h3>
            </div>
            <hr />
            <div className = "bundleBody">
                <img src = {imgPath} />
                <OptionalContainer includedAttributes={includedAttributes} />
            </div>
            
        </div>
    )
}

export default Bundle;
