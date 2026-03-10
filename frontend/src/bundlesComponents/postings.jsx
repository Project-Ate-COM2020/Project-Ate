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
import "./bundles.css";

/* --- Test Data Declarations --- */
const bundles = [
    {
    bundleName: "Big Cheese Bundle",
    bundleCategory: "Dairy",
    imgPath: "/Dairy.jpg",
    pickupTime: "11:00 - 12:00",
    seller: "Cheesy Goods Incorporated",
    price: 14.50,
    location: "Exeter",
    stock: 56,
    },
    {
    bundleName: "Big Bertha Bread Bundle",
    bundleCategory: "Bakery",
    imgPath: "/Bakery.jpg",
    pickupTime: "15:00 - 16:00",
    seller: "Big Bang Bakery",
    price: 9.67,
    location: "York",
    stock: 17,
    },
    {
    bundleName: "Dreamy Dessert Drops",
    bundleCategory: "Desserts",
    imgPath: "/Desserts.jpg",
    pickupTime: "13:00 - 14:00",
    seller: "Daddy Dick's Desserts",
    price: 16.99,
    location: "Bristol (LPP)",
    stock: 100,
    },
    {
    bundleName: "Fresh Veggie Delight",
    bundleCategory: "Fresh Produce",
    imgPath: "/Fresh_Produce.jpg",
    pickupTime: "09:00 - 10:00",
    seller: "Vegan Veggie Vascular Fanatics",
    price: 10.00,
    location: "London",
    stock: 45,
    },
    {
    bundleName: "Hot To Go",
    bundleCategory: "Hot Meals",
    imgPath: "/Hot_Meals.jpg",
    pickupTime: "10:00 - 11:00",
    seller: "Hot Hattie's Hella Good Meals",
    price: 19.99,
    location: "Exmouth",
    stock: 56,
    },
    {
    bundleName: "Sassy Salsa Salad Selection",
    bundleCategory: "Prepared Salads",
    imgPath: "/Prepared_Salads.jpg",
    pickupTime: "14:00 - 15:00",
    seller: "Sally's Sallads",
    price: 5.99,
    location: "Leeds",
    stock: 100,
    },
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
    let moreInfoButtonDisplayed = false;

    for (const i of includedAttributes) {
        if (i === "pickup time") {pickupTimeDisplayed = true;}
        if (i === "bundle category") {bundleCategoryDisplayed = true;}
        if (i === "seller") {sellerDisplayed = true;}
        if (i === "price") {priceDisplayed = true;}
        if (i === "location") {locationDisplayed = true;}
        if (i === "stock") {stockDisplayed = true;}
        if (i === "more info button") {moreInfoButtonDisplayed = true;}
    }

    return (
        <div className = "bundleContainer">

            <h3>{bundleData.bundleName}</h3>

            <img src = {bundleData.imgPath} alt = {bundleData.bundleName} />

            {pickupTimeDisplayed && <p>pickup time: {bundleData.pickupTime}</p>}

            {bundleCategoryDisplayed && <p>Bundle Category: {bundleData.bundleCategory}</p>}

            {sellerDisplayed && <p>Seller: {bundleData.seller}</p>}

            {priceDisplayed && <p>Price: £{bundleData.price}</p>}

            {locationDisplayed && <p>Location: {bundleData.location}</p>}

            {stockDisplayed && <p>Stock: {bundleData.stock}</p>}

            {moreInfoButtonDisplayed && <button>More Info</button>}

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