import React from "react";
import NavBar from "../reusableComponents/navBar.jsx";


// This will now be the profile the seller sees

// Based on Will's design I need the following components:
/* 
MVP:
The location they are currently viewing
Company Information
Stats
Forecasts
Add new bundle button

1st Sprint:
2 seller analytics from seeded data
1 baseline forecast
current bundles waiting for collection (include a complete button for when buyer picks up bundle)

2nd Sprint:
More forecasting algorithms
Full analytics
Current bundles on display
Complaints section with the ability to respond

AS OF 02/02/2026 I am going to create a design template with some software,
then implement MVP, then first sprint before pull requesting this branch hopefully today
*/


function SellerHomePage(){
    return(
    <div>
    <div>
        <NavBar />
    </div>
    <div>
        <SellerInfo />
        <Analytics />
        <ReservedBundles />
        <ForecastsNewBundles />
    </div>
    </div>
    );

}// for the views - rather than create inside this dir I will create inside the respective pages dirs to avoid confusion

export default SellerHomePage;