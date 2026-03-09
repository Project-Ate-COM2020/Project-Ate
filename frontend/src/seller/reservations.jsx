/* --- File Description --- */
/* IDK Mate should be self explanatory */

/* --- Current Issues --- */

/* The main issue is the current backend bug preventing from loggin in - this means when the backend is fixed 
and endpoints refactored, the endpoints and maybe the parsing for this file will also need to change */

/* --- Import Statements --- */
import NavBar from "../reusableComponents/navBar.jsx";
import Bundles from "../bundlesComponents/bundles.jsx";

/* --- Main Page Function --- */
function Reservation() {
    return (
        <div>
            <NavBar />
            <Bundles includedAttributes={["buyer", "more info button"]}/>
        </div>
    )
}

export default Reservation;