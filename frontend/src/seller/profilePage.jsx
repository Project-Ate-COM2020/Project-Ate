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

/* --- Main Page Function --- */
function ProfilePage() {
    const [editMode, setEditMode] = useState(false);

    // Testing values, these will be replaced with hooks to desired endpoints 
    const sellerName = "Frontend Test Name";
    const accountLifetime = "Frontend Test Lifetime";
    const location = "Frontend Test Location";
    const openingHours = "Frontend Test Opening Hours"

    const infoContainer = (
        <div className = "Info container">                
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

                <div className = "Edit button">
                    <button onClick={() => setEditMode(true)}>
                        Edit Info
                    </button>
                </div>
        </div>
    )
    
    const editInfoContainer = (
        <div className = "Edit info container">

        </div>
    )

    if (!editMode) {
        return (
            <div>
                <NavBar />
                {infoContainer}
            </div>
        );
    } else {
        return (
            <div>
                <NavBar />
                {editInfoContainer}
            </div>
        );
    }
}

// The main page is the only export
export default ProfilePage;