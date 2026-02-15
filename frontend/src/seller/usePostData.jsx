import { useState } from 'react';

// Hook for making POST requests
// Returns a function to execute the POST request, along with data, loading, and error states

function usePostData(endpoint) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(false);

    const postData = async (body = {}) => {
        try {
            setLoading(true);

            const url = `http://127.0.0.1:8000/${endpoint}`;
            
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(body),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const APIdata = await response.json();
            setData(APIdata);
            return APIdata;
        } catch (e) {

            setData(null);
            throw e;
        } finally {
            setLoading(false);
        }
    };

    return { postData, data, loading };
}

export default usePostData;
