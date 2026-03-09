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
const bundles = [
    {
    bundleName: "Big Cheese Bundle",
    bundleCategory: "Dairy",
    imgPath: "/Dairy.jpg",
    pickupTime: "11:00 - 12:00",
    seller: "Cheesy Goods Incorporated",
    price: 14.5,
    location: "Exeter",
    stock: 56,
    },
  ];

/* --- Helper Functions  --- */
function SingleBundle({bundleData, includedAttributes = []}) {

    let pickupTimeDisplayed = false;
    let bundleCategoryDisplayed = false;
    let sellerDisplayed = false;
    let priceDisplayed = false;
    let locationDisplayed = false;
    let stockDisplayed = false;
    let reserveBundleButtonDisplayed = false;

    for (const i of includedAttributes) {
        if (i === "pickup time") {pickupTimeDisplayed = true;}
        if (i === "bundle category") {bundleCategoryDisplayed = true;}
        if (i === "seller") {sellerDisplayed = true;}
        if (i === "price") {priceDisplayed = true;}
        if (i === "location") {locationDisplayed = true;}
        if (i === "stock") {stockDisplayed = true;}
        if (i === "reserve bundle button") {reserveBundleButtonDisplayed = true;}
    }

    return (
        <div className = "bundleContainer">
            <img src = {bundleData.imgPath} alt = {bundleData.bundleName} />

            <h3>{bundleData.bundleName}</h3>

            {pickupTimeDisplayed && <p>pickup time: {bundleData.pickupTime}</p>}

            {bundleCategoryDisplayed && <p>Bundle Category: {bundleData.bundleCategory}</p>}

            {sellerDisplayed && <p>Seller: {bundleData.seller}</p>}

            {priceDisplayed && <p>Price: £{bundleData.price}</p>}

            {locationDisplayed && <p>Location: {bundleData.location}</p>}

            {stockDisplayed && <p>Stock: {bundleData.stock}</p>}

            {reserveBundleButtonDisplayed && <button>Reserve bundle</button>}

        </div>
    )
}

/* --- Main Page Function --- */
function Bundles({includedAttributes=[], numberOfBundles = 1, endPoint = "", postBody = {}}) {
    return (
        <div className = "postingsContainer">
            {bundles.slice(0, numberOfBundles).map((bundle, index) => (
                <SingleBundle
                    key={`${bundle.bundleName}-${index}`}
                    bundleData={bundle}
                    includedAttributes={includedAttributes}
                />
            ))}
        </div>
    )
}

export default Bundles;