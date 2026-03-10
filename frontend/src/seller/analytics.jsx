/* --- Description --- */
/* Analytics means analytics */

/* --- Current Issues --- */

/* The main issue is the current backend bug preventing from loggin in - this means when the backend is fixed 
and endpoints refactored, the endpoints and maybe the parsing for this file will also need to change */

/* --- Import Statements --- */
import './analytics.css';
import NavBar from '../reusableComponents/navBar';

/* --- Test Data Declarations --- */
const numListings = 142;
const numReservations = 97;
const amountRevenue = 2436.50;
const percentageListingsCollected = 84;
const noShowRate = 11;
const avgRevenuePerListing = 17.16;


function Analytics() {
    return (
        <div>
        <NavBar user_type = {"seller"}/>
        <div className="analytics-panel">
            <h2>All time Analytics</h2>

            <h3>Total number of listings posted</h3>
            <p>{numListings}</p>

            <h3>Total number of reservations made</h3>
            <p>{numReservations}</p>

            <h3>Total amount of revenue generated</h3>
            <p>£{amountRevenue}</p>

            <h3>Percentage of postings collected</h3>
            <p>{percentageListingsCollected}%</p>

            <h3>Percentage of noshows for reserved listings</h3>
            <p>{noShowRate}%</p>

            <h3>Average amount of revenue generated per listing</h3>
            <p>£{avgRevenuePerListing}</p>
        </div>
        </div>
    )
}

export default Analytics;