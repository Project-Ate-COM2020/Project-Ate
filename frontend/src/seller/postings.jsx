/* --- File Description --- */
/* IDK Mate should be self explanatory */

/* --- Current Issues --- */

/* The main issue is the current backend bug preventing from loggin in - this means when the backend is fixed 
and endpoints refactored, the endpoints and maybe the parsing for this file will also need to change */

/* --- Import Statements --- */
import NavBar from "../reusableComponents/navBar.jsx";
import Postings from "../bundlesComponents/postings.jsx";

/* --- Main Page Function --- */
function Reservation() {
    return (
        <div>
            <NavBar />
            <Postings />
        </div>
    )
}

export default Reservation;