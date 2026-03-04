/* --- Import Statements --- */
import { useState, useEffect } from 'react';

/* --- File Description --- */
/* This will be a universal function that will take a path and arguments then return json data, this 
is being used so only this library needs to interact with logic such as jwt auth tokens and token refreshing,
meaning all other code can be abstracted making for easier development */

/* --- Main Function Declaration --- */
function useGetData(endpoint, queryParams = {}) {
    // define variables with state
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);


    /* --- Defining the UseEffect Hook --- */
    useEffect(function() {
        // Parse query parameters dictionary to create query string
        // uses proper URI encoding to prevent any invalid queries that could threaten security
        let queryString = "";
        if (Object.keys(queryParams).length !== 0) {
            queryString = "?";
            for (let param in queryParams) {
                queryString += encodeURIComponent(param) + "=" + encodeURIComponent(queryParams[param]) + "&";
            }
            queryString = queryString.slice(0, -1);
        }

        /* --- Async Function to Fetch Data --- */
        async function fetchData() {
            try {
                // Uses HardCoded localhost URL - may need to be changed in production
                // Includes authorisation
                const token = localStorage.getItem('access_token');
                let response = null;
                if (token != null) {
                    response = await fetch("http://localhost:8000/" + endpoint + queryString, {
                    headers: { "Authorization" : "Bearer " + token} 
                });
                }
                else {
                    response = await fetch("http://localhost:8000/" + endpoint + queryString); 
                }
                const json = await response.json();
                setData(json);
                setLoading(false);
            // Simple error catching - logs the file to the console
            } catch (err) {
                setLoading(false);
                console.log("ERROR - Could not fetch API Data (check arguments calling get.jsx)");
            }
        }
        fetchData();
    }, [endpoint, queryParams]);

    return { data, loading };
}

export default useGetData;