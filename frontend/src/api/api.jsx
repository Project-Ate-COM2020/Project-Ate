/* --- Import Statements --- */
import { useState, useEffect } from 'react';

/* --- File Description --- */
/* This will be a universal library - hopefully encompasses all API communication needed for the remainder of the project.
This is split into hooks - used for statistics, part of webpage like badges and auto updated things relying on backend data; and
async functions - these can be called on the submission of a form to allow the user to interact with the backend e.g reserving a bundle */

/* --- Current Issues --- */

/* Need to finish the refreshToken function and integrate it into the rest of the library to allow the program
to automatically refresh invalid tokens */

// Need to parse response for return code - for better error handling

/* --- Helper Functions --- */
function buildQueryString(queryParams = {}) {
    let queryString = "";
    if (Object.keys(queryParams).length !== 0) {
        queryString = "?";
        for (let param in queryParams) {
            queryString += encodeURIComponent(param) + "=" + encodeURIComponent(queryParams[param]) + "&";
        }
        queryString = queryString.slice(0, -1);
    }
    return queryString;
}

async function refreshTokens() {
    response = await fetch("http://localhost:8000/", {
        method : "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body : {
            "refresh": localStorage.getItem("access_token")
        }
    });

    const tokens = await response.json();

    if (tokens.access) localStorage.setItem("access_token", tokens.access);
    if (tokens.refresh) localStorage.setItem("refresh_token", tokens.refresh);
}

/* --- Get/Post Functions --- */
async function getData(endpoint, queryParams = {}, authenticate) {
    try {
        const queryString = buildQueryString(queryParams);
        const token = localStorage.getItem("access_token");
        const include_auth = (token != null) && (authenticate == true);

        let response = null;
        if (include_auth) {
            response = await fetch("http://localhost:8000/" + endpoint + queryString, {
                headers: {
                    "Authorization": "Bearer " + token,
                    "Content-Type": "application/json"
                },
            });
        }
        else {
            response = await fetch("http://localhost:8000/" + endpoint + queryString, {
                headers: {
                    "Content-Type": "application/json"
                },
            });
        }

        return await response.json();
    } catch (err) {
        console.log("ERROR - Could not fetch API Data (check arguments calling get.jsx)");
    }
}

async function postData(endpoint, postData, authenticate) {
    try {
        const token = localStorage.getItem('access_token');
        const include_auth = (token != null) && (authenticate == true);

        let response = null;
        if (include_auth) {
            response = await fetch("http://localhost:8000/" + endpoint + "/", {
                method : "POST",
                headers: {
                    "Authorization": "Bearer " + token,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(postData)
            });
        }
        else {
            response = await fetch("http://localhost:8000/" + endpoint + "/", {
                method : "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(postData)
            });
        }
    
    return await response.json();

    } catch (err) {
        console.log("ERROR - Could not fetch API Data (check arguments calling get.jsx)");
    }
}


/* --- Get/Post Hooks --- */
function useGetData(endpoint, queryParams = {}, authenticate) {
    // define variables with state
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    /* --- Defining the UseEffect Hook --- */
    useEffect(function() {
        // Parse query parameters dictionary to create query string
        // uses proper URI encoding to prevent any invalid queries that could threaten security

        setLoading(true);

        const queryString = buildQueryString(queryParams);

        /* --- Async Function to Fetch Data --- */
        async function fetchData() {
            try {
                // Uses HardCoded localhost URL - may need to be changed in production
                // Includes authorisation in header format, assumes they are stored in secure local storage
                const token = localStorage.getItem('access_token');
                let response = null;
                const include_auth = (token != null) && (authenticate == true);
                if (include_auth) {
                    response = await fetch("http://localhost:8000/" + endpoint + queryString, {
                        headers: { 
                            "Authorization" : "Bearer " + token,
                            "Content-Type": "application/json"
                        },
                    });
                }
                else {
                    response = await fetch("http://localhost:8000/" + endpoint + queryString, {
                        headers: { 
                            "Content-Type": "application/json"
                        },
                    }); 
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

/* --- Final Exports --- */
export { getData, useGetData, postData, usePostData };