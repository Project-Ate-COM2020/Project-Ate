/* Lists all the available bundle postings to the user */
import fakeBundles from "./fakeBundles";
import { useEffect, useMemo, useState } from "react"; /* It imports the different react hooks  */


export default function Listings() {
  const [bundles, setBundles] = useState([]); /* It is a hook that stores the bundles and the function to load bundles from memory */ 
  const [loading, setLoading] = useState(true);/* It stores a true or false value depending on which toggle to use*/ 

  // manual toggle: if clicked forces to user fake bundles instead of real bundles 
  const [useFake, setUseFake] = useState(false); 

  // This is the Auto fall back if the API fails
  const [apiFailed, setApiFailed] = useState(false); 

  const [selectedBundleId, setSelectedBundleId] = useState(null);
 

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

  // find the selected bundle object so the info data is correct for it 
  const selectedBundle = useMemo(() => {
    if (selectedBundleId == null) return null;
    return bundlesToShow.find((b) => b.id === selectedBundleId) || null;
  }, [selectedBundleId, bundlesToShow]);



  // POST OP to redeem code

  async function redeemBundleCode(bundleId){
    try {
      // Fake mode
      if (useFake || apiFailed){
        alert(`FAKE Bundle ${bundleId} redeemed`);
        return;
      }
      

      //Real POST - Edit when you have got the backend 
      const res = await fetch("/api/marketplace/orders/redeem", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },

      credentials: "include", // keep if using Django sessions
      body: JSON.stringify({
        bundle_id: bundleId,
      }),
    });

      if (!res.ok){
        const text = await res.text();
        throw new Error(text || `HTTP ${res.status}`);
      }

      const data = await res.json();
      alert(`Redeemed successfully! Order ID: ${data.order_id ?? "OK"}`);
    } catch (err) {
      alert(`Redeem failed: ${err.message}`);
    }
  }

  function toggleInfo(bundleId) {
    setSelectedBundleId((current) => (current === bundleId ? null : bundleId));
  }

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

      {/*info dropdown panel that pushes the list down */}
      {selectedBundle && (
        <div
          style={{
            border: "1px solid #ddd",
            borderRadius: 8,
            padding: 12,
            marginBottom: 12,
          }}
        >
          <div style={{display: "flex", justifyContent: "space-between", gap: 12}}>
            <div>
              <h3 style={{margin: 0}}>{selectedBundle.name}</h3>
              <p style={{ margin: "6px 0" }}>£{selectedBundle.price}</p>
            </div>

          <button onClick={() => setSelectedBundleId(null)}>Close</button>
          </div>

          <p style={{ margin: "8px 0" }}>
            <strong>Company:</strong> {selectedBundle.company ?? "—"}
          </p>
          <p style={{ margin: "8px 0" }}>
            <strong>Collection location:</strong> {selectedBundle.collectionLocation ?? "—"}
          </p>
          <p style={{ margin: "8px 0" }}>
            <strong>Expiry date:</strong> {selectedBundle.expiryDate ?? "—"}
          </p>
          <p style={{ margin: "8px 0" }}>
            <strong>Allergens:</strong>{" "}
            {Array.isArray(selectedBundle.allergens) && selectedBundle.allergens.length > 0
              ? selectedBundle.allergens.join(", ")
              : "None listed"}
          </p>

          {selectedBundle.description && (
            <p style={{ margin: "8px 0" }}>
              <strong>Description:</strong> {selectedBundle.description}
            </p>
          )}
        </div>
      )}


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
            <button onClick={() => toggleInfo(bundle.id)}>
              {selectedBundleId === bundle.id ? "Hide info" : "Info"}
            </button>

              <button onClick={() =>  redeemBundleCode(bundle.id)}>
                Redeem code
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
