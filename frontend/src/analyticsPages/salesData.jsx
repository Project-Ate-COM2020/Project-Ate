import { fetchSalesData } from "../api/analytics";

function SalesData() {
    const [salesData, setSalesData] = useState(null);
    useEffect(() => {
            // defines an async function for asynchronous data fetching using 'await'
            const loadData = async () => {
                // sets state of loading to true
                setLoading(true);
                // calls the api function asynchronously
                const sales = await fetchSalesData();
                // sets the state variables with fetched data
                setSalesData(sales);
                // sets state of loading to false 
                setLoading(false);
            };
            loadData();
            // empty dependency array means this runs once on component mount
        }, []);
    // if the state of loading is true, display loading message
    if (loading) 
        return (
            <div>
                <h3>Loading sales data...</h3>
            </div>
        );

    return (
        <div>
        <h1>Sales Data:</h1>
        <p>{salesData ? JSON.stringify(salesData) : "No data available"}</p>
        </div>
    )
}

export default SalesData;