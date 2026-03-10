// Trying to globalise some of the code I used previously in forecasting and analytics in this new refactored seller environment to speed up the development process
// so far this is only useful to return a single line of text from the API - I can't really make it parse JSON, for future use I will convert it into a custom hook
import { useState, useEffect } from 'react';


function LoadTextDataGetRequest( {endpoint, queryParams}) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const loadData = async ( {endpoint, queryParams}) => {
        try {
            setLoading(true);

            // format parameters for request
            let queryString = "";
            if (Object.keys(queryParams).length !== 0) {
                for (let param in queryParams) {
                    let paramString = "";
                    paramString = `${param}=${queryParams[param]}`;
                    queryString += paramString;
                    queryString += "&"
                }
                queryString = queryString.slice(0, -1);
            } else {
                queryString = null;
            }

            let response ;
            
            // fetch the data itself
            if (queryString !== null) {
                response = await fetch(`http://127.0.0.1:8000/${endpoint}/?${queryString}`);
            } else {
                response = await fetch(`http://127.0.0.1:8000/${endpoint}`);
            }
            
            
            // proper error checking as this function will be used quite a lot by me
            if (!response.ok) {
            const text = await response.text();
            throw new Error(`HTTP ${response.status}: ${text}`);
            }

            const APIdata = await response.json();
            setData(APIdata);
        } catch (e) {
            setData(null);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
    loadData({ endpoint: endpoint, queryParams: queryParams });
    }, [endpoint, queryParams]);

    if (loading === true) {
        return (
            <p>Loading...</p>
        )
    }

    if (data !== null) {
        return(
            data
        )
    }

    return (
        <p>ERROR - THIS SHOULD NOT HAPPEN</p>
    )

}

export default LoadTextDataGetRequest;