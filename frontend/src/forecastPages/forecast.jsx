import React, { use, useEffect, useState } from "react";
import NavBar from "../reusableComponents/navBar.jsx";

function ForecastPage(){
    const [forecasts, setForecasts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [bundleCategory, setBundleCategory] = useState("");
    const [pickupTime, setPickupTime] = useState("");
    const [weather, setWeather] = useState("");
    const [dayOfTheWeek, setDayOfTheWeek] = useState("");
    const [sellerID, setSellerID] = useState(""); // You'll need to set this appropriately

    // get API data using api/.js helpers
    useEffect(() => {
        const loadData = async () => {
            setLoading(true);
            const response = await fetch("/forecast/forecast-prediction?sellerID="+sellerID+"&bundleCategory="+bundleCategory+"&pickupTime="+pickupTime+"&weather="+weather+"&dayOfTheWeek="+dayOfTheWeek);
            const data = await response.json();
            setForecasts(data);
            setLoading(false);
        };
        
        loadData();
    }, [sellerID, bundleCategory, pickupTime, weather, dayOfTheWeek]);
    
    // now forecasts will contain the fetched data from /forecasts endpoint THIS IS NOT NEARLY FINISHED ONLY FOR OWN DEV



    return(
        <div>
            <div>
                <NavBar />
            </div>
            <div>
                <title>Sales Forecast Page</title>
                <h1>Sales Forecasts for: {sellerID}</h1>
                <hr />
                <div>
                    <select value={pickupTime} onChange={(e) => setPickupTime(e.target.value)}>
                            <option value="">Select an option</option>
                            <option value="09:00-10:00">9-10</option>
                            <option value="10:00-11:00">10-11</option>
                            <option value="11:00-12:00">11-12</option>
                    </select>
                    <hr />
                    <select value={bundleCategory} onChange={(e) => setBundleCategory(e.target.value)}>
                            <option value="Bakery">Bakery</option>
                            <option value="Hot Meals">Hot Meals</option>
                            <option value="Fresh Produce">Fresh Produce</option>
                            <option value="Dairy">Dairy</option>
                            <option value="Prepared Salads">Prepared Salads</option>
                            <option value="Deserts">Deserts</option>
                    </select>
                    <hr />
                    <select value={weather} onChange={(e) => setWeather(e.target.value)}>
                            <option value={0}>Sunny</option>
                            <option value={1}>Raining</option>
                    </select>
                    <hr />
                    <select value={dayOfTheWeek} onChange={(e) => setDayOfTheWeek(e.target.value)}>
                            <option value={"Monday"}>Monday</option>
                            <option value={"Tuesday"}>Tuesday</option>
                            <option value={"Wednesday"}>Wednesday</option>
                            <option value={"Thursday"}>Thursday</option>
                            <option value={"Friday"}>Friday</option>
                            <option value={"Saturday"}>Saturday</option>
                            <option value={"Sunday"}>Sunday</option>
                    </select>
                </div>
                <hr />
            </div>
        </div>
    );
}

export default ForecastPage;