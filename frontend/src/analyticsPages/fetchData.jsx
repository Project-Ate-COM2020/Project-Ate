import { useState, useEffect } from "react";
import { fetchSalesData, fetchRevenueData, fetchNoShowData } from "../api/analytics";

// good example of reusable code, I would add it to a reUsable components Dir, but I think other people would prefer different methods for invoking API calls

// defining main function of component
function FetchData( {dataEntry} ) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
            // defines an async function for asynchronous data fetching using 'await'
            const loadData = async () => {
                // sets state of loading to true
                setLoading(true);
                // calls the api function asynchronously
                // uses a switch case function to chose the correct api function based on dataEntry argument
                let data = null;
                switch (dataEntry) {
                    case 'sales':
                        data = await fetchSalesData();
                        break;
                    case 'revenue':
                        data = await fetchRevenueData();
                        break;
                    case 'noShows':
                        data = await fetchNoShowData();
                        break;
                    default:
                        console.error("Invalid data entry:", dataEntry);
                        return <div>Invalid data entry: {dataEntry}</div>;
                }
                setData(data);
                // sets state of loading to false 
                setLoading(false);
            };
            loadData();
            // includes dataEntry so it refetches when the prop changes
        }, [dataEntry]);
    
    // if the state of loading is true, display loading message
    if (loading) 
        return (
            <div>
                <h3>Loading data...</h3>
            </div>
        );

    // else, return data
    return (
        <div>
        <h1>{dataEntry} Data:</h1>
        <p>{JSON.stringify(data)}</p>
        </div>
    )
}

export default FetchData;