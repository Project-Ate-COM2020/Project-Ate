// importing api functions to fetch data
import FetchData from "./fetchData";
import NavBar from "../components/NavBar";

// defining main function of component
function Analytics() {
    // defining constants to hold fetched data and loading state


    // data is displayed without any formatting for now - will refine later
    // simple checks to make sure data is available before trying to display it "No data available" message otherwise
    return (
        <div>
        <title>Seller Analytics</title>
        < NavBar />
        <h1>Analytics</h1>
        <hr />
        <FetchData dataEntry="sales" />
        <hr />
        <FetchData dataEntry="revenue" />
        <hr />
        <FetchData dataEntry="noShows" />
        <hr />
        <h2>Repeat for other metrics we track</h2>
        <p>GET DATA</p>
        </div>
    )
}

export default Analytics;