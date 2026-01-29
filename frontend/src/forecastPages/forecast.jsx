import React from "react";
import NavBar from "../reusableComponents/navBar.jsx";

function ForecastPage(){
    return(
    <div>
    <div>
        <NavBar />
    </div>
    <div>
        <title>Sales Forecast Page</title>
        <h1>Sales Forecasts for: GET SELLER NAME</h1>
        <hr />
        <h2>Forecast Overview:</h2>
        <p>GET FORECAST DATA</p>
        <hr />
    </div>
    </div>
    );

}

export default ForecastPage;