import React, { useEffect, useState } from "react";
import NavBar from "../reusableComponents/navBar.jsx";

function ForecastPage(){
    const [forecasts, setForecasts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [bundleCategory, setBundleCategory] = useState("");
    const [pickupTime, setPickupTime] = useState("");
    const [weather, setWeather] = useState("");
    const [dayOfTheWeek, setDayOfTheWeek] = useState("");
    const [sellerID, setSellerID] = useState("");
    const [noBundles, setNoBundles] = useState(0);

    // get API data using api/.js helpers

    // need to globalise this reusable code
    const loadData = async () => {
        setLoading(true);
        const response = await fetch("/forecast/forecast-prediction?sellerID="+sellerID+"&bundleCategory="+bundleCategory+"&pickupTime="+pickupTime+"&weather="+weather+"&dayOfTheWeek="+dayOfTheWeek);
        const data = await response.json();
        setForecasts(data);
        setLoading(false);
    }
    // now forecasts will contain the fetched data from /forecasts endpoint THIS IS NOT NEARLY FINISHED ONLY FOR OWN DEV

    let reservations_avg = "";
    let noShows_avg = "";

    if (loading) {
        reservations_avg = "Loading...";
        noShows_avg = "loading...";
    } else {
        reservations_avg = forecasts.reservation_avg;
        noShows_avg = forecasts.noShow_avg;
    }

    return(
        <div>
            <div>
                <NavBar />
            </div>
            <div>
                <h1>Sales Forecasts for: {sellerID}</h1>
                <hr />
                <div>
                    <select value={pickupTime} onChange={(e) => setPickupTime(e.target.value)}>
                        <option value="00:00-01:00">0-1am</option>
                        <option value="01:00-02:00">1-2am</option>
                        <option value="02:00-03:00">2-3am</option>
                        <option value="03:00-04:00">3-4am</option>
                        <option value="04:00-05:00">4-5am</option>
                        <option value="05:00-06:00">5-6am</option>
                        <option value="06:00-07:00">6-7am</option>
                        <option value="07:00-08:00">7-8am</option>
                        <option value="08:00-09:00">8-9am</option>
                        <option value="09:00-10:00">9-10am</option>
                        <option value="10:00-11:00">10-11am</option>
                        <option value="11:00-12:00">11-12pm</option>
                        <option value="12:00-13:00">12-1pm</option>
                        <option value="13:00-14:00">1-2pm</option>
                        <option value="14:00-15:00">2-3pm</option>
                        <option value="15:00-16:00">3-4pm</option>
                        <option value="16:00-17:00">4-5pm</option>
                        <option value="17:00-18:00">5-6pm</option>
                        <option value="18:00-19:00">6-7pm</option>
                        <option value="19:00-20:00">7-8pm</option>
                        <option value="20:00-21:00">8-9pm</option>
                        <option value="21:00-22:00">9-10pm</option>
                        <option value="22:00-23:00">10-11pm</option>
                        <option value="23:00-00:00">11-12am</option>                    
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
                    <p>Expected weather conditions</p>
                    <select value={weather} onChange={(e) => setWeather(e.target.value)}>
                        <option value={0}>Sunny</option>
                        <option value={1}>Raining</option>
                    </select>
                    <hr />
                    <p>Day of the week available</p>
                    <select value={dayOfTheWeek} onChange={(e) => setDayOfTheWeek(e.target.value)}>
                        <option value={1}>Monday</option>
                        <option value={2}>Tuesday</option>
                        <option value={3}>Wednesday</option>
                        <option value={4}>Thursday</option>
                        <option value={5}>Friday</option>
                        <option value={6}>Saturday</option>
                        <option value={7}>Sunday</option>
                    </select>
                    <hr />
                    <p>No. Bundles to sell</p>
                    <input type="number" min="0" placeholder="" value={noBundles} onChange={(e) => setNoBundles(e.target.value)} />
                    <hr />
                    <button onClick={loadData}>Load Forecasts</button>
                </div>
                <hr />
                <div>
                    <h2>Number of expected reservations</h2>
                    <p>{reservations_avg}</p>
                    <h2>Number of expected no shows</h2>
                    <p>{noShows_avg}</p>
                </div>
            </div>
        </div>
    );
}

export default ForecastPage;