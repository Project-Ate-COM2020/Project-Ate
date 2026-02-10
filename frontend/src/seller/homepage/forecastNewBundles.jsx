import { useState } from "react";

function ForecastNewBundles() {

    // Biggest bit yet, need to make creation of bundles + forecasting
    // I will need to code a new mechanic to make a post request for post requests

    /* Bundle Creation
    Value - Bundle Name
    Value - Bundle Category
    value - Contents
    value - Allergens
    value - Quantity
    value - Pickup Window

    button - Generate suggested price

    output - Suggested Price

    value - Price

    output - Predicted number of reservations

    button - Post bundle

    */

    const [bundleName, setBundleName] = useState("");
    const [bundleCategory, setCategory] = useState("");
    const [contents, setContents] = useState("");
    const [allergens, setAllergens] = useState("");
    const [quantity, setQuantity] = useState("");
    const [pickupWindow, setPickupWindow] = useState("");
    const [price, setPrice] = useState(0);


    return (
        <div>
            <h3>Bundle Creation</h3>
            <input type="text" name ="bundleName" onChange={(e) => setBundleName(e.target.value)} ></input>
            <input type="text" name ="bundleCategory" onChange={(e) => setCategory(e.target.value)} ></input>
            <input type="text" name ="contents" onChange={(e) => setContents(e.target.value)} ></input>
            <input type="text" name ="allergens" onChange={(e) => setAllergens(e.target.value)} ></input>
            <input type="text" name ="quantity" onChange={(e) => setQuantity(e.target.value)} ></input>
            <input type="text" name ="pickupWindow" onChange={(e) => setPickupWindow(e.target.value)} ></input>
            <input type="text" name ="price" onChange={(e) => setPrice(e.target.value)} ></input>
        </div>

    )

}

export default ForecastNewBundles