// I will be duplicating a lot of code from other branches here but oh well

// Analytics I will start with:
// Total listings, total reservations, total revenue
// percentage of listings collected
// No show rate
// Average revenue per listing
// Average revenue per reservation

import useLoadData from '../loadDataHook.jsx';
import './analytics.css';

function Analytics() {
    const { data: totalListings, loading: loadingListings } = useLoadData('analytics/totalListings', { sellerID: 1 });
    const { data: totalReservations, loading: loadingReservations } = useLoadData('analytics/totalReservations', { sellerID: 1 });
    const { data: totalNoShows, loading: loadingNoShows } = useLoadData('analytics/totalNoshows', { sellerID: 1 });
    const { data: totalRevenue, loading: loadingRevenue } = useLoadData('analytics/totalRevenue', { sellerID: 1 });

    // now define the values for every statistic we will display

    let numListings;
    let numReservations;
    let amountRevenue;
    let percentageListingsCollected;
    let noShowRate;
    let avgRevenuePerListing;


    // Total number of listings
    if (loadingListings) {
        numListings = "Loading..."
    } else { numListings = totalListings }

    // Total number of reservations
    if (loadingReservations){
        numReservations = "Loading..."
    } else { numReservations = totalReservations}

    // Total Revenue
    if (loadingRevenue) {
        amountRevenue = "Loading..."
    } else { amountRevenue = totalRevenue}

    // percentage of listings collected
    if (loadingListings || loadingReservations || loadingNoShows) {
        percentageListingsCollected = "Loading..."
    } else {
        let totalUnreserved = totalListings - totalReservations;
        let totalUncollected = totalUnreserved + totalNoShows;
        percentageListingsCollected = 100 * (totalUncollected / totalListings)
    }

    // no show rate
    if (loadingReservations || loadingNoShows) {
        noShowRate = "Loading..."
    } else {
        noShowRate = 100 * (totalNoShows/totalReservations)
    }

    // avg revenue per listing
    if (loadingListings || loadingRevenue) {
        avgRevenuePerListing = "Loading...";
    } else {
        avgRevenuePerListing = 100 * (totalRevenue / totalListings)
    }

    return (
        <div className="analytics-panel">
            <h2>All time Analytics</h2>

            <h3>Total number of listings posted</h3>
            <p>{numListings}</p>

            <h3>Total number of listings reserved by a buyer</h3>
            <p>{numReservations}</p>

            <h3>Total amount of revenue generated</h3>
            <p>{amountRevenue}</p>

            <h3>Percentage of listings collected</h3>
            <p>{percentageListingsCollected}%</p>

            <h3>Percentage of noshows for reserved listings</h3>
            <p>{noShowRate}%</p>

            <h3>Average amount of revenue generated per listing</h3>
            <p>{avgRevenuePerListing}</p>
        </div>
    )



}

export default Analytics;