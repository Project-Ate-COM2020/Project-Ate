/* --- File Description --- */
/* IDK Mate should be self explanatory */

/* --- Current Issues --- */

/* The main issue is the current backend bug preventing from loggin in - this means when the backend is fixed 
and endpoints refactored, the endpoints and maybe the parsing for this file will also need to change */

/* --- Import Statements --- */
import NavBar from "../reusableComponents/navBar.jsx";
import Posting from "../bundlesComponents/posting.jsx";
import { useNavigate } from "react-router-dom";

/* --- Main Page Function --- */
function Reservation() {
    const navigate = useNavigate();
    return (
        <div>
            <NavBar user_type = {"seller"}/>
            <Posting includedAttributes={["stock", "pickup time", "location", "price", "allergens"]} backFunction={() => navigate("/seller/postings")} />
        </div>
    )
}

export default Reservation;