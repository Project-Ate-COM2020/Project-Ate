import NavBar from "../reusableComponents/navBar.jsx";
import Listings from "../reusableComponents/listings.jsx";

function UserHomePage(){
    return(
    <>
        <NavBar />
        <Listings/>
        <div>Home page works</div>
    </>
    );

}

export default UserHomePage;