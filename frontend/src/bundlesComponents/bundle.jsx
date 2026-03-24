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

/* --- Helper Functions --- */
function OptionalContainer({ includedAttributes, bundleData, unreserveBundleFunction, markCollectedFunction }) {

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
        if (i == "pickup time" || i == "Pickup time") {pickupTimeDisplayed = true;}
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
            {pickupTimeDisplayed && <p>Pickup time: {bundleData.pickupTime}</p>}

            {bundleCategoryDisplayed && <p>Bundle Category: {bundleData.bundleCategory}</p>}

            {sellerDisplayed && <p>Seller: {bundleData.seller}</p>}

            {buyerDisplayed && <p>Buyer: {bundleData.buyer}</p>}

            {collectionCodeDisplayed && <p>Collection Code: {bundleData.collectionCode}</p>}

            {priceDisplayed && <p>Price: £{bundleData.price}</p>}

            {locationDisplayed && <p>Location: {bundleData.location}</p>}

            {markCollectedButtonDisplayed && <button onClick = {markCollectedFunction}>Mark Bundle as collected</button>}

            {unreserveBundleButtonDisplayed && <button onClick = {unreserveBundleFunction}>Unreserve bundle</button>}

            
        </div>
    )
}

/* --- Main Function --- */
function Bundle({ includedAttributes = [], backfunction, bundleData = {}, unreserveBundleFunction, markCollectedFunction }) {
    const bundleName = bundleData.bundleName || "Bundle";

    return (
        <div className = "bundleDisplay">
            <button className="bundleCloseButton" onClick={backfunction}>X</button>
            <div className = "bundleTitle">
                <h3>{bundleName}</h3>
            </div>
            <hr />
            <div className = "bundleBody">
                <img src = {bundleData.imgPath || ""} alt={bundleName} />
                <OptionalContainer includedAttributes={includedAttributes} bundleData={bundleData} unreserveBundleFunction={unreserveBundleFunction} markCollectedFunction={markCollectedFunction}/>
            </div>
            
        </div>
    )
}

export default Bundle;
