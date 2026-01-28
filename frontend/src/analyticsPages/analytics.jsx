import React, { useState, useEffect } from "react";
import { fetchSalesData, fetchNoShowData, fetchRevenueData } from "../api/analytics";

function Analytics() {
    const [salesData, setSalesData] = useState(null);
    const [noShowData, setNoShowData] = useState(null);
    const [revenueData, setRevenueData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadAnalytics = async () => {
            setLoading(true);
            const sales = await fetchSalesData();
            const noShows = await fetchNoShowData();
            const revenue = await fetchRevenueData();
            setSalesData(sales);
            setNoShowData(noShows);
            setRevenueData(revenue);
            setLoading(false);
        };

        loadAnalytics();
    }, []);

    if (loading) return <div>Loading analytics...</div>;


    // data is displayed without any formatting for now - will refine later
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