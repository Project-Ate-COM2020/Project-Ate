import React, { use, useEffect, useState } from "react";
import NavBar from "../reusableComponents/navBar.jsx";

function ForecastPage(){
    const [forecasts, setForecasts] = useState([]);


    // get API data using api/.js helpers
    const loadData = async () => {
        const [data, setData] = useState(null);
        const [loading, setLoading] = useState(true);
        useEffect(() => {
            const loadData = async () => {
                setLoading(true);
                const response = await fetch("/forecasts"); // need to connect to json to get all forecast data
                const data = await response.json();
                setForecasts(data);
                setLoading(false);
            }
        }, []);
    }
    
    // now forecasts will contain the fetched data from /forecasts endpoint THIS IS NOT NEARLY FINISHED ONLY FOR OWN DEV

    return(
        <div>
            <div>
                <NavBar />
            </div>
            <div>
                <title>Sales Forecast Page</title>
                <h1>Sales Forecasts for: GET SELLER NAME</h1>
                <hr />
                
                <div>
                </div>
                <hr />
            </div>
        </div>
    );
}

export default ForecastPage;