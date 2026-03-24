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
import "./posting.css";

/* --- Helper Functions --- */
function OptionalContainer({ includedAttributes, postingData, reserveBundleFunction }) {

    let pickupTimeDisplayed;
    let bundleCategoryDisplayed;
    let sellerDisplayed;
    let stockDisplayed;
    let priceDisplayed;
    let locationDisplayed;
    let reserveBundleButtonDisplayed;
    let allergensDisplayed;

    for (const i of includedAttributes) {
        if (i == "pickup time" || i == "Pickup time") {pickupTimeDisplayed = true;}
        if (i == "bundle category") {bundleCategoryDisplayed = true;}
        if (i == "seller") {sellerDisplayed = true;}
        if (i == "price") {priceDisplayed = true;}
        if (i == "location") {locationDisplayed = true;}
        if (i == "reserve bundle button") {reserveBundleButtonDisplayed = true;}
        if (i == "stock") {stockDisplayed = true;}
        if (i == "allergens") {allergensDisplayed = true;}
    }

    return (
        <div className = "infoContainer">
            {pickupTimeDisplayed && <p>Pickup time: {postingData.pickupTime}</p>}

            {bundleCategoryDisplayed && <p>Bundle Category: {postingData.bundleCategory}</p>}

            {sellerDisplayed && <p>Seller: {postingData.seller}</p>}

            {priceDisplayed && <p>Price: £{postingData.price}</p>}

            {locationDisplayed && <p>Location: {postingData.location}</p>}

            {stockDisplayed && <p>Stock: {postingData.stock}</p>}

            {allergensDisplayed && (
                <p>
                    {(postingData.allergens ?? []).length === 0
                        ? "Contains: None declared"
                        : "Contains: " + (postingData.allergens ?? []).join(", ")}
                </p>
            )}

            {reserveBundleButtonDisplayed && <button onClick = {reserveBundleFunction}>Reserve bundle</button>}

        </div>
    )
}

/* --- Main Function --- */
function Bundle({ includedAttributes = [], backFunction, postingData = {}, reserveBundleFunction }) {
    const bundleName = postingData.bundleName || "Bundle";

    return (
        <div className = "postingDisplay">
            <button className="postingCloseButton" onClick={backFunction}>X</button>
            <div className = "postingTitle">
                <h3>{bundleName}</h3>
            </div>
            <hr />
            <div className = "postingBody">
                <img src = {postingData.imgPath || ""} alt={bundleName} />
                <OptionalContainer includedAttributes={includedAttributes} postingData={postingData} reserveBundleFunction={reserveBundleFunction} />
            </div>
            
        </div>
    )
}

export default Bundle;