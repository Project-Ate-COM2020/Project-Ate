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
import "./bundles.css"

/* --- Test Data Declarations --- */
const bundles = [
    {
      bundleName: "Big Cheese Bundle",
      bundleCategory: "Dairy",
      imgPath: "/Dairy.jpg",
      pickupTime: "11:00 - 12:00",
      seller: "Cheesy Goods Incorporated",
      buyer: "Bobby",
      collectionCode: "QWERTY",
      price: 14.5,
      location: "Exeter",
    },
  ];

/* --- Helper Functions  --- */
function SingleBundle({bundleData, includedAttributes = [], moreInfoButtonFunction}) {

    let pickupTimeDisplayed = false;
    let bundleCategoryDisplayed = false;
    let sellerDisplayed = false;
    let buyerDisplayed = false;
    let collectionCodeDisplayed = false;
    let priceDisplayed = false;
    let locationDisplayed = false;
    let moreInfoButtonDisplayed = false;

    for (const i of includedAttributes) {
        if (i === "pickup time") {pickupTimeDisplayed = true;}
        if (i === "bundle category") {bundleCategoryDisplayed = true;}
        if (i === "seller") {sellerDisplayed = true;}
        if (i === "buyer") {buyerDisplayed = true;}
        if (i === "collection code") {collectionCodeDisplayed = true;}
        if (i === "price") {priceDisplayed = true;}
        if (i === "location") {locationDisplayed = true;}
        if (i === "more info button") {moreInfoButtonDisplayed = true;}
    }

    return (
        <div className = "bundleContainer">

            <h3>{bundleData.bundleName}</h3>

            <img src = {bundleData.imgPath} alt = {bundleData.bundleName} />

            {pickupTimeDisplayed && <p>pickup time: {bundleData.pickupTime}</p>}

            {bundleCategoryDisplayed && <p>Bundle Category: {bundleData.bundleCategory}</p>}

            {sellerDisplayed && <p>Seller: {bundleData.seller}</p>}

            {buyerDisplayed && <p>Buyer: {bundleData.buyer}</p>}

            {collectionCodeDisplayed && <p>Collection Code: {bundleData.collectionCode}</p>}

            {priceDisplayed && <p>Price: £{bundleData.price}</p>}

            {locationDisplayed && <p>Location: {bundleData.location}</p>}

            {moreInfoButtonDisplayed && (
                <button onClick={() => moreInfoButtonFunction?.(bundleData)}>More Info</button>
            )}

        </div>
    )
}

/* --- Main Page Function --- */
function Bundles({bundles: bundlesProp = [], includedAttributes=[], numberOfBundles = 1, endPoint = "", postBody = {}, moreInfoButtonFunction}) {
    const bundlesToDisplay = bundlesProp.length > 0 ? bundlesProp : bundles;

    return (
        <div className = "bundlesContainer">
            {bundlesToDisplay.slice(0, numberOfBundles).map((bundle) => (
                <SingleBundle
                    key={bundle.collectionCode ?? `${bundle.bundleName}-${bundle.pickupTime}`}
                    bundleData={bundle}
                    includedAttributes={includedAttributes}
                    moreInfoButtonFunction={moreInfoButtonFunction}
                />
            ))}
        </div>
    )
}

export default Bundles;