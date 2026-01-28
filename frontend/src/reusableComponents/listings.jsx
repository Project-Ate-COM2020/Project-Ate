/* Lists all the available bundle postings to the user */

import { useEffect, useMemo, useState } from "react"; /* It imports the different react hooks  */

export default function Listings() {
  const [bundles, setBundles] = useState([]); /* It is a hook that stores the bundles and the function to load bundles from memory */ 
  const [loading, setLoading] = useState(true);/* It stores a true or false value depending on which toggle to use*/ 

  // manual toggle: if clicked forces to user fake bundles instead of real bundles 
  const [useFake, setUseFake] = useState(false); 

  // This is the Auto fall back if the API fails
  const [apiFailed, setApiFailed] = useState(false); 

  // The client side data to test bundles before connecting it to the backend.
  const fakeBundles = [
    { id: 1, name: "Student Bundle", price: 9.99 },
  { id: 2, name: "Meal Prep Bundle", price: 14.50 },
  { id: 3, name: "Family Bundle", price: 24.99 },
  { id: 4, name: "Fitness Bundle", price: 19.99 },
  { id: 5, name: "Vegan Starter Bundle", price: 16.99 },
  { id: 6, name: "Protein Power Bundle", price: 21.50 },
  { id: 7, name: "Budget Saver Bundle", price: 7.99 },
  { id: 8, name: "Gourmet Dinner Bundle", price: 29.99 },
  { id: 9, name: "Breakfast Boost Bundle", price: 11.49 },
  { id: 10, name: "Quick Lunch Bundle", price: 12.99 },
  { id: 11, name: "Kids Favourites Bundle", price: 18.75 },
  { id: 12, name: "Low Carb Bundle", price: 20.00 },
  { id: 13, name: "Gluten-Free Bundle", price: 17.99 },
  { id: 14, name: "High Energy Bundle", price: 22.49 },
  { id: 15, name: "Weekend Feast Bundle", price: 34.99 },
  { id: 16, name: "Office Lunch Bundle", price: 13.99 },
  ];

  // This a an async function that loads the bundles whilst the rest of the page loads 
  useEffect(() => {
    async function loadBundles() {
      try {
        setLoading(true);
        setApiFailed(false);

        // **************************************************
        const res = await fetch("/api/marketplace/bundles");
        //*************************************************** -> need update to cnnect to the backend 


        // allows you to debug if there is any issues connecting to django backend 
        if (!res.ok) throw new Error(`HTTP ${res.status}`);

        // converts data into json 
        const data = await res.json(); 

        // If backend returns empty list return error message and use fake bundles 
        if (!Array.isArray(data) || data.length === 0) {
          setApiFailed(true);
          setBundles([]);
        } else {
          setBundles(data);
        }
      } catch (err) {
        console.error("Failed to load bundles:", err);
        setApiFailed(true);
        setBundles([]);
      } finally {
        setLoading(false);
      }
    }

    loadBundles();
  }, []);

  // Decide which bundle to use real or fake but doing a cache calculation 
  // only re does the calculation if any of the 3 var changes in the array below 
  const bundlesToShow = useMemo(() => {
    if (useFake || apiFailed) return fakeBundles;
    return bundles;
  }, [useFake, apiFailed, bundles]);
  
  return (
    <div style={{ padding: 16, maxWidth: 600 }}>
      <h2>Available Bundles</h2>

      {/* Toggle + status */}
      <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 12 }}>
        <label style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <input
            type="checkbox"
            checked={useFake}
            onChange={(e) => setUseFake(e.target.checked)}
          />
          Use fake bundles
        </label>

        {loading && <span>Loading…</span>}

        {!loading && apiFailed && !useFake && (
          <span style={{ fontSize: 12 }}>
            API unavailable/empty → showing fake bundles
          </span>
        )}

        {!loading && !apiFailed && !useFake && (
          <span style={{ fontSize: 12 }}>
            Showing API bundles
          </span>
        )}
      </div>

      {/* Scrollable list container */}
      <div
        style={{
          maxHeight: 320,          // controls how tall before scrolling
          overflowY: "auto",       // enables scroll wheel / trackpad scrolling
          border: "1px solid #ddd",
          borderRadius: 8,
          padding: 12,
        }}
      >
        {bundlesToShow.map((bundle) => (
          <div
            key={bundle.id}
            style={{
              borderBottom: "1px solid #eee",
              padding: "12px 0",
            }}
          >
            <h3 style={{ margin: "0 0 6px 0" }}>{bundle.name}</h3>
            <p style={{ margin: "0 0 10px 0" }}>£{bundle.price}</p>

            <div style={{ display: "flex", gap: 8 }}>
              <button onClick={() => alert(`Info for bundle ${bundle.id}`)}>
                Info
              </button>

              <button onClick={() => alert(`Add bundle ${bundle.id} to cart`)}>
                Add to Cart
              </button>
            </div>
          </div>
        ))}

        {bundlesToShow.length === 0 && !loading && (
          <p style={{ margin: 0 }}>No bundles available.</p>
        )}
      </div>
    </div>
  );
}
