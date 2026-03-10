/* --- File Description --- */
/* As Per Will's design, this page is very simple - and only 
needs 2 parts - display seller details and edit seller details */

/* --- Current Issues --- */

/* The main issue is the current backend bug preventing from loggin in - this means when the backend is fixed 
and endpoints refactored, the endpoints and maybe the parsing for this file will also need to change */

/* --- Import Statements --- */
import { useGetData, usePostData, postData } from "../reusableComponents/api.jsx";
import { useEffect, useState } from "react";
import NavBar from "../reusableComponents/navBar.jsx";
import "./profilePage.css";

/* --- Helper Functions --- */

function saveChanges() {
    // Will use the pstData function imported to submit the form to the backend to change seller details
}

/* --- Main Page Function --- */

function SellerProfilePage() {
    const [editMode, setEditMode] = useState(false);

    // Testing values, these will be replaced with hooks to desired endpoints 
    const sellerName = "Frontend Test Name";
    const accountLifetime = "Frontend Test Lifetime";
    const location = "Frontend Test Location";
    const openingHours = "Frontend Test Opening Hours"

    // This will be a simple page w one container, that varies between 2, I will define both here, and the stateful variable 'editMode' will define which is returned

    const infoContainer = (
        <div className = "infoContainer">                
                <div className = "Info">
                    <p>Seller Name:</p>
                    <p>{sellerName}</p>
                </div>
                
                <div className = "Info">
                    <p>Account Lifetime:</p>
                    <p>{accountLifetime}</p>
                </div>

                <div className = "Info">
                    <p>Location:</p>
                    <p>{location}</p>
                </div>

                <div className = "Info">
                    <p>Opening Hours:</p>
                    <p>{openingHours}</p>
                </div>

                <div className = "editButton">
                    <button onClick={() => setEditMode(true)}>
                        Edit Info
                    </button>
                </div>
        </div>
    )
    
    const editInfoContainer = (
        <div className = "infoContainer">
            
                <div className = "Info">
                    <p>Seller Name:</p>
                    <input type = "text" defaultValue = {sellerName}></input>
                </div>

                <div className = "Info">
                    <p>Location:</p>
                    <input type = "text" defaultValue = {location}></input>
                </div>

                <div className = "Info">
                    <p>Opening Hours:</p>
                    <input type = "text" defaultValue = {openingHours}></input>
                </div>

                <div className = "saveButton">
                    <button onClick={saveChanges}>
                        Save Changes
                    </button>
                </div>

                <div className = "cancelButton">
                    <button onClick={() => setEditMode(false)}>
                        Discard Changes
                    </button>
                </div>
        </div>
    )

    if (!editMode) {
        return (
            <div className = "sellerProfilePage">
                <NavBar />
                {infoContainer}
            </div>
        );
    } else {
        console.log("Switch SUccessful");
        return (
            <div className = "sellerProfilePage">
                <NavBar />
                {editInfoContainer}
            </div>
        );
    }
}

// The main page is the only export
export default SellerProfilePage;