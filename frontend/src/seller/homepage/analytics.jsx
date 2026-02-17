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
    const { data: listingsData, loading: loadingListings } = useLoadData('analytics/total-listings', { seller_id: 1 });
    const { data: reservationsData, loading: loadingReservations } = useLoadData('analytics/total-reservations', { seller_id: 1 });
    const { data: noShowsData, loading: loadingNoShows } = useLoadData('analytics/total-no-shows', { seller_id: 1 });
    const { data: revenueData, loading: loadingRevenue } = useLoadData('analytics/total-revenue', { seller_id: 1 });
    const { data: collectedReservationsData, loading: loadingCollectedReservations } = useLoadData('analytics/collected-reservations', { seller_id: 1 });

    // Extract values from response objects (handle both nested and plain responses)
    const totalListings = typeof listingsData === 'number' ? listingsData : (listingsData?.total_listings ?? 0);
    const totalReservations = typeof reservationsData === 'number' ? reservationsData : (reservationsData?.total_reservations ?? 0);
    const totalNoShows = typeof noShowsData === 'number' ? noShowsData : (noShowsData?.total_no_shows ?? 0);
    const totalRevenue = typeof revenueData === 'number' ? revenueData : (revenueData?.total_revenue ?? 0);

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
    if (loadingListings || loadingCollectedReservations) {
        percentageListingsCollected = "Loading..."
    } else {
        const denominator = totalListings || 0;
        if (denominator === 0) {
            percentageListingsCollected = 0;
        } else {
            percentageListingsCollected = ((collectedReservationsData) / (collectedReservationsData + totalNoShows) * 100).toFixed(2);
        }
    }

    // no show rate
    if (loadingReservations || loadingNoShows) {
        noShowRate = "Loading..."
    } else {
        const denominator = totalReservations || 0;
        noShowRate = denominator === 0 ? 0 : (totalNoShows / denominator * 100).toFixed(2);
    }

    // avg revenue per listing
    if (loadingListings || loadingRevenue) {
        avgRevenuePerListing = "Loading...";
    } else {
        const denominator = totalListings || 0;
        avgRevenuePerListing = denominator === 0 ? 0 : (totalRevenue / denominator).toFixed(2);
    }

    return (
        <div className="analytics-panel">
            <h2>All time Analytics</h2>

            <h3>Total number of listings posted</h3>
            <p>{numListings}</p>

            <h3>Total number of reservations made</h3>
            <p>{numReservations}</p>

            <h3>Total amount of revenue generated</h3>
            <p>{amountRevenue}</p>

            <h3>Percentage of postings collected</h3>
            <p>{percentageListingsCollected}%</p>

            <h3>Percentage of noshows for reserved listings</h3>
            <p>{noShowRate}%</p>

            <h3>Average amount of revenue generated per listing</h3>
            <p>{avgRevenuePerListing}</p>
        </div>
    )



}

export default Analytics;