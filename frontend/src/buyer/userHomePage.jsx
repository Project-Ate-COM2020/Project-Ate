import NavBar from "../reusableComponents/navBar.jsx";
import Postings from "../bundlesComponents/postings.jsx";

function UserHomePage(){
    return(
    <>
        <NavBar />
        <Postings includedAttributes = {["price", "more info button"]} numberOfBundles = {50}/>
    </>
    );

}

export default UserHomePage;