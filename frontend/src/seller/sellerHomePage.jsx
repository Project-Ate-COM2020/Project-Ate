import React from "react";
import NavBar from "../reusableComponents/navBar.jsx";


function SellerHomePage(){
    return(
    <div>
    <div>
        <NavBar />
    </div>
    <div>
        <title>Home Page</title>
        <h1>You are: GET SELLER NAME</h1>
        <hr />
        <h2>current listing overview:</h2>
        <p>GET LISTING DATA</p>
        <hr />
        <h2>Recent reservations overview:</h2>
        <p>GET RESERVATION DATA</p>
        <hr />
        <h2>Sales Analytics:</h2>
        <p>GET SALES DATA</p>
        <hr />
        <h2>Sales Forecasts:</h2>
        <p>GET FORECAST DATA</p>
        <hr />
    </div>
    </div>
    );

}// for the views - rather than create inside this dir I will create inside the respective pages dirs to avoid confusion

export default SellerHomePage;