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

/* Currently, the refreshTokens function has no way to determine whether
the user is a buyer or a seller, either refresh tokens endpoints need to 
be merged or more likely I need to store this fact in cookies */

const api = import.meta.env.VITE_API_HOST;
const port = import.meta.env.VITE_API_PORT;

const base = `http://${api}:${port}`;

console.log(base)

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
    console.log("STARTING TOKEN REFRESHING");
    const user_type = localStorage.getItem("user_type");
    console.log(user_type);
    let response = null;
    if (user_type === "seller") {
        response = await fetch(`${base}/auth/refresh`, {
            method : "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body : JSON.stringify({
                "refresh": localStorage.getItem("refresh_token")
            })
            
        });
    } else if (user_type === "buyer") {
        response = await fetch(`${base}/auth/refresh`, {
            method : "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body : JSON.stringify({
                "refresh": localStorage.getItem("refresh_token")
            })
            
        });
    } else {return false;}

    const tokens = await response.json();

    console.log("TOKEN BEING REFRESHED");

    if (tokens.access) {
        localStorage.setItem("access_token", tokens.access)
        console.log("TOKEN REFRESHED");
        };

    return !!tokens.access;
}

/* --- Get/Post Functions --- */
async function getData(endpoint, queryParams = {}, authenticate = true) {
    try {
        const queryString = buildQueryString(queryParams);
        const token = localStorage.getItem("access_token");
        const include_auth = (token != null) && (authenticate == true);

        let response = null;
        if (include_auth) {
            for (let i = 0; i < 4; i++) {
                const token = localStorage.getItem("access_token");
                response = await fetch(`${base}/` + endpoint + queryString, {
                    headers: {
                        "Authorization": "Bearer " + token,
                        "Content-Type": "application/json"
                    },
                });

                if (response.status !== 401 && response.status !== 403) {
                    console.log("THIS API THINKS RESPONSE IS CORRECT");
                    break;
                }
                console.log("THIS API THINKS RESPONSE IS INCORRECT");

                const refreshed = await refreshTokens();
                if (!refreshed) break;
            }
        }
        else {
            response = await fetch(`${base}` + endpoint + queryString, {
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

async function postData(endpoint, postData, authenticate = true) {
    try {
        const token = localStorage.getItem('access_token');
        const include_auth = (token != null) && (authenticate == true);
        let response = null;

        // Tries to access data, if tokens invalid then refreshes and tries again
        if (include_auth) {
            for (let i = 0; i < 4; i++) {
                const token = localStorage.getItem("access_token");
                response = await fetch(`${base}/`  + endpoint, {
                    method: "POST",
                    headers: {
                        "Authorization": "Bearer " + token,
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(postData),
                });

                if (response.status !== 401 && response.status !== 403) {
                    console.log("THIS API THINKS RESPONSE IS CORRECT");
                    break;
                }
                console.log("THIS API THINKS RESPONSE IS INCORRECT");

                const refreshed = await refreshTokens();
                if (!refreshed) break;
            }
        }
        else {
            response = await fetch(`${base}/` + endpoint, {
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

async function putData(endpoint, putData, authenticate = true) {
    try {
        const token = localStorage.getItem('access_token');
        const include_auth = (token != null) && (authenticate == true);
        let response = null;

        // Tries to access data, if tokens invalid then refreshes and tries again
        if (include_auth) {
            for (let i = 0; i < 4; i++) {
                const token = localStorage.getItem("access_token");
                response = await fetch(`${base}/`  + endpoint, {
                    method: "PUT",
                    headers: {
                        "Authorization": "Bearer " + token,
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(putData),
                });

                if (response.status !== 401 && response.status !== 403) {
                    console.log("THIS API THINKS RESPONSE IS CORRECT");
                    break;
                }
                console.log("THIS API THINKS RESPONSE IS INCORRECT");

                const refreshed = await refreshTokens();
                if (!refreshed) break;
            }
        }
        else {
            response = await fetch(`${base}/` + endpoint, {
                method : "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(putData)
            });
        }
    
    return await response.json();

    } catch (err) {
        console.log("ERROR - Could not fetch API Data (check arguments calling get.jsx)");
    }
}

async function deleteData(endpoint, authenticate = true) {
    try {
        const token = localStorage.getItem('access_token');
        const include_auth = (token != null) && (authenticate == true);
        let response = null;

        // Tries to access data, if tokens invalid then refreshes and tries again
        if (include_auth) {
            for (let i = 0; i < 4; i++) {
                const token = localStorage.getItem("access_token");
                response = await fetch(`${base}/`  + endpoint, {
                    method: "DELETE",
                    headers: {
                        "Authorization": "Bearer " + token,
                        "Content-Type": "application/json",
                    },
                });

                if (response.status !== 401 && response.status !== 403) {
                    console.log("THIS API THINKS RESPONSE IS CORRECT");
                    break;
                }
                console.log("THIS API THINKS RESPONSE IS INCORRECT");

                const refreshed = await refreshTokens();
                if (!refreshed) break;
            }
        }
        else {
            response = await fetch(`${base}/` + endpoint, {
                method : "DELETE",
                headers: {
                    "Content-Type": "application/json"
                }
            });
        }

    if (response.status === 204) {
        return null;
    }

    return await response.json();

    } catch (err) {
        console.log("ERROR - Could not fetch API Data (check arguments calling get.jsx)");
    }
}



/* --- Get/Post Hooks --- */
function useGetData(endpoint, queryParams = {}, authenticate = true ) {
    // define variables with state
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const queryString = buildQueryString(queryParams);

    /* --- Defining the UseEffect Hook --- */
    useEffect(function() {
        // Parse query parameters dictionary to create query string
        // uses proper URI encoding to prevent any invalid queries that could threaten security

        setLoading(true);

        /* --- Async Function to Fetch Data --- */
        async function fetchData() {
            try {
                // Uses HardCoded localhost URL - may need to be changed in production
                // Includes authorisation in header format, assumes they are stored in secure local storage
                const token = localStorage.getItem('access_token');
                let response = null;
                const include_auth = (token != null) && (authenticate == true);
                if (include_auth) {
                    for (let i = 0; i < 4; i++) {
                        const token = localStorage.getItem('access_token');
                        response = await fetch(`${base}/` + endpoint + queryString, {
                            headers: { 
                                "Authorization" : "Bearer " + token,
                                "Content-Type": "application/json"
                            },
                        });

                        if (response.status !== 401 && response.status !== 403) break;

                        const refreshed = await refreshTokens();
                        if (!refreshed) break;
                    }
                }
                else {
                    response = await fetch(`${base}/` + endpoint + queryString, {
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
    }, [endpoint, queryString, authenticate]);

    return { data, loading };
}

function usePostData(endpoint, postData, authenticate = true ) {
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
                    for (let i = 0; i < 4; i++) {
                        const token = localStorage.getItem('access_token');
                        response = await fetch(`${base}/` + endpoint + "/", {
                            method: "POST",
                            headers: { 
                                "Authorization" : "Bearer " + token,
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify(postData)                           
                        });
                        
                        if (response.status !== 401 && response.status !== 403) break;

                        const refreshed = await refreshTokens();
                        if (!refreshed) break;
                    }
                }
                else {
                    response = await fetch(`${base}/` + endpoint + "/", {
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
export { getData, postData, putData, deleteData, usePostData, useGetData };