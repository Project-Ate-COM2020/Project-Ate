/* --- File Description --- */
/* IDK Mate should be self explanatory */

/* --- Current Issues --- */

/* The main issue is the current backend bug preventing from loggin in - this means when the backend is fixed 
and endpoints refactored, the endpoints and maybe the parsing for this file will also need to change */

/* --- Import Statements --- */
import NavBar from "../reusableComponents/navBar.jsx";
import Postings from "../bundlesComponents/postings.jsx";
import { useNavigate } from "react-router-dom";

/* --- Main Page Function --- */
function Reservation() {
    const navigate = useNavigate();
    return (
        <div>
            <NavBar user_type = {"seller"}/>
            <Postings includedAttributes={["stock", "more info button"]} numberOfBundles={18} moreInfoButtonFunction={() => navigate("/seller/posting")}/>
        </div>
    )
}

export default Reservation;