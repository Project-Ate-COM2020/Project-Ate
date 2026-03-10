import { useState } from "react";
// import "./forecastNewBundles.css";
import usePostData from "../usePostData";

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

    const { postData: suggestPrice, loading: suggestLoading } = usePostData("endpoint1/");
    const { postData: createBundle, loading: createLoading } = usePostData("endpoint2/");

    return (
        <div className = "bundleCreation-panel">
            <h3>Bundle Creation</h3>
            <p>Bundle Name</p>
            <input type="text" name ="bundleName" onChange={(e) => setBundleName(e.target.value)} ></input>
            <p>Bundle Category</p>
            <input type="text" name ="bundleCategory" onChange={(e) => setCategory(e.target.value)} ></input>
            <p>Contents</p>
            <input type="text" name ="contents" onChange={(e) => setContents(e.target.value)} ></input>
            <p>Allergens</p>
            <input type="text" name ="allergens" onChange={(e) => setAllergens(e.target.value)} ></input>
            <p>Quantity</p>                
            <input type="text" name ="quantity" onChange={(e) => setQuantity(e.target.value)} ></input>
            <p>Pickup Window</p>
            <input type="text" name ="pickupWindow" onChange={(e) => setPickupWindow(e.target.value)} ></input>

            <button>Generate Suggested price</button>
            <p>Suggested price: {suggestedPrice}</p>

            <p>Price</p>
            <input type="text" name ="price" onChange={(e) => setPrice(e.target.value)} ></input>

            <button>Create Posting</button>
            <p>Suggested price: {suggestedPrice}</p>
        </div>

    )

}

export default ForecastNewBundles