import { useEffect, useState } from 'react';

// basically the same as the load data function except I made it into a hook, this allows me to do some calculations to the data on the frontend

function useLoadData(endpoint, queryParams = {}) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadData = async () => {
            try {
                setLoading(true);

                // format parameters for request
                let queryString = "";
                if (Object.keys(queryParams).length !== 0) {
                    for (let param in queryParams) {
                        queryString += `${param}=${queryParams[param]}&`;
                    }
                    queryString = queryString.slice(0, -1);
                }

                // fetch the data
                const url = queryString 
                    ? `http://127.0.0.1:8000/${endpoint}/?${queryString}`
                    : `http://127.0.0.1:8000/${endpoint}/`;
                
                const response = await fetch(url);

                const APIdata = await response.json();
                setData(APIdata);
            } catch (e) {
                setData(null);
            } finally {
                setLoading(false);
            }
        };

        loadData();
    }, [endpoint, JSON.stringify(queryParams)]);

    return { data, loading };
}

export default useLoadData;