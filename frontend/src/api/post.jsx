/* --- Import Statements --- */
import { useState, useEffect } from 'react';

/* --- File Description --- */
/* This is very similar to the get file, except for post requests */

/* --- Current Issues --- */
// This Hook updates every time the reference changes, to improve performance move to checking value rather than reference
// Need to parse response for return code - for better error handling

/* --- Main Function Declaration --- */
function usePostData(endpoint, postData, authenticate) {
    // define variables with state
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);


    /* --- Defining the UseEffect Hook --- */
    useEffect(function() {
        // Parse query parameters dictionary to create query string
        // uses proper URI encoding to prevent any invalid queries that could threaten security

        setLoading(true);

        /* --- Async Function to Fetch Data --- */
        async function fetchData() {
            try {
                // Uses HardCoded localhost URL - may need to be changed in production
                // Includes authorisation
                const token = localStorage.getItem('access_token');
                let response = null;
                const include_auth = (token != null) && (authenticate == true);
                if (include_auth) {
                    response = await fetch("http://localhost:8000/" + endpoint + "/", {
                        method: "POST",
                        headers: { 
                            "Authorization" : "Bearer " + token,
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify(postData)
                        
                    });
                }
                else {
                    response = await fetch("http://localhost:8000/" + endpoint + "/", {
                        headers: { 
                            "Content-Type": "application/json"
                        },
                        method: "POST",
                        body: JSON.stringify(postData)
                    }); 
                }
                const json = await response.json();
                setData(json);
                setLoading(false);
            // Simple error catching - logs the file to the console
            } catch (err) {
                setLoading(false);
                console.log("ERROR - Could not fetch API Data (check arguments calling post.jsx)");
            }
        }
        fetchData();
    }, [endpoint, postData]);

    return { data, loading };
}

export default usePostData;