// importing react libraries to assign variables with state
import React, { useState, useEffect } from "react";
// importing api functions to fetch data
import { fetchSalesData, fetchNoShowData, fetchRevenueData } from "../api/analytics";

// defining main function of component
function Analytics() {
    // defining constants to hold fetched data and loading state
    const [salesData, setSalesData] = useState(null);
    const [noShowData, setNoShowData] = useState(null);
    const [revenueData, setRevenueData] = useState(null);
    const [loading, setLoading] = useState(true);

    // this is the hook that gets data from api using api funcions
    useEffect(() => {
        // defines an async function for asynchronous data fetching using 'await'
        const loadAnalytics = async () => {
            // sets state of loading to true
            setLoading(true);
            // calls the api function asynchronously
            const sales = await fetchSalesData();
            const noShows = await fetchNoShowData();
            const revenue = await fetchRevenueData();
            // sets the state variables with fetched data
            setSalesData(sales);
            setNoShowData(noShows);
            setRevenueData(revenue);
            setLoading(false);
        };

        loadAnalytics();
        // empty dependency array means this runs once on component mount
    }, []);

    // if the state of loading is true, display loading message
    if (loading) return <div>Loading analytics...</div>;


    // data is displayed without any formatting for now - will refine later
    // simple checks to make sure data is available before trying to display it "No data available" message otherwise
    return (
        <div>
        <title>Seller Analytics</title>
        <h1>Analytics</h1>
        <hr />
        <h2>Sales Data:</h2>
        <p>{salesData ? JSON.stringify(salesData) : "No data available"}</p>
        <hr />
        <h2>Percentage No shows:</h2>
        <p>{noShowData ? JSON.stringify(noShowData) : "No data available"}</p>
        <hr />
        <h2>Total revenue</h2>
        <p>{revenueData ? JSON.stringify(revenueData) : "No data available"}</p>
        <hr />
        <h2>Repeat for other metrics we track</h2>
        <p>GET DATA</p>
        </div>
    )
}

export default Analytics;