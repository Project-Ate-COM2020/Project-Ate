/* Lists all the available bundle postings to the user */
import "./listings.css";
import fakeBundles from "./fakeBundles";
import { addFakeOrder, makeClaimCode, getFakeOrders, removeFakeOrder } from "./fakeOrdersStore";
import { useEffect, useMemo, useState } from "react"; /* It imports the different react hooks  */
import { fetchMarketplaceBundles, fetchMarketplaceOrders } from "../api/marketplace";
import { requestJson } from "../api/authorisation";

/*lists all the avable bundle postings to the user*/

// Automatically assumes the state is listings unless metioned elsewhere 
export default function Listingsv2({ mode = "listings" }) {
  const isOrders = mode === "orders"; /*changes the mode when on the /orders page*/

  const [bundles, setBundles] = useState([]); /* It is a hook that stores the bundles and the function to load bundles from memory */ 
  const [loading, setLoading] = useState(true);/* It stores a true or false value depending on which toggle to use*/ 

  // manual toggle for fake and real data for testing purposes 
  const [useFake, setUseFake] = useState(false); 

  // This is the Fall back if the API fails 
  const [apiFailed, setApiFailed] = useState(false); 

  // stores which bundle has been selected for the info button to appear 
  const [selectedBundleId, setSelectedBundleId] = useState(null);

  // version counters forcing react to upadate when the remove button is pressed 
  const [fakeOrdersVersion, setFakeOrdersVersion] = useState(0);
  const [ordersVersion, setOrdersVersion] = useState(0);


  // This a an async function that loads the bundles whilst the rest of the page loads 
  useEffect(() => {
    async function loadBundles() {
      try {
        setLoading(true);
        setApiFailed(false);

        const data = isOrders
          ? await fetchMarketplaceOrders()
          : await fetchMarketplaceBundles();

        console.log("isOrders:", isOrders);
        console.log("raw API data:", data);

        // normalizes orders and bundles 
        const normalised = isOrders
          ? (data.reservations || data)  // Extract reservations array if wrapped
          : data.map((p) => ({
              id: p.posting_id,
              name: `${p.category} bundle`,
              price: p.price,
              company: "—",
              collectionLocation: "—",
              expiryDate: p.pickup_window,
              allergens: p.allergens,
              description: p.contents,
            }));
        
        console.log("NORMALISED: ");
        console.log(normalised);

        // Check if response is valid array (empty array is valid - means no orders/bundles)
        if (!Array.isArray(normalised)) {
          setApiFailed(true);
          setBundles([]);
          console.log("API response is not an array");
        } else {
          setBundles(normalised);  // Set bundles even if empty array
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
  }, [isOrders, ordersVersion]);


  // updates the react components when the variables in the [] change on the webpage 
  const bundlesToShow = useMemo(() => {
    if (isOrders) {
      if (useFake) return getFakeOrders();
      if (apiFailed) return getFakeOrders();   // fallback
      return bundles;
    }
  
    if (useFake || apiFailed) return fakeBundles;
    return bundles;
  }, [isOrders, useFake, apiFailed, bundles, fakeOrdersVersion]);

  // find the selected bundle object so the info data is correct for it 
  const selectedBundle = useMemo(() => {
    if (selectedBundleId == null) return null;
    return bundlesToShow.find((b) => b.id === selectedBundleId) || null;
  }, [selectedBundleId, bundlesToShow]);


  // POST OP to redeem code

  async function redeemBundleCode(bundleId) {
    try {
      console.log("HELLOOO");
      console.log(bundleId);
      // Find the bundle object (needed for fake orders)
      const bundle = bundlesToShow.find((b) => b.id === bundleId);
      if (!bundle) {
        alert("Bundle not found");
        return;
      }
  
      // FAKE MODE
      if (useFake || apiFailed) {
        const claim = makeClaimCode();
  
        addFakeOrder({
          order_id: Date.now(),              // fake unique id
          claim_code: claim,
          status: "RESERVED",
          created_at: new Date().toISOString(),
  
          // store full bundle info so Orders page can render it
          ...bundle,
        });
  
        alert(`(FAKE) Order created!\nCode: ${claim}`);
        return;
      }
  
      // REAL MODE (backend)
      const data = await requestJson("/buyer/reservebundle/", {
        method: "POST",
        body: {
          posting_id: bundleId,
          consumer_id: 1,
        },
      });

      alert(`Redeemed successfully! Reservation ID: ${data.reservation_id ?? "OK"}`);
    } catch (err) {
      alert(`Redeem failed: ${err.message}`);
    }
  }

  //detirmines if a bundles info is on display or not and toggles between the close and the info button
  function toggleInfo(bundleId) {
    setSelectedBundleId((current) => (current === bundleId ? null : bundleId));
  }

  // return orders back to stock 
  async function returnOrderToStock(order) {
    try{
      if(!order) return;

      if(useFake || apiFailed){
        const orderId = order.order_id ?? order.reservation_id;
        if(orderId == null){
          alert("Can't remove order: missing ID");
          return;
        }
        removeFakeOrder(orderId);
        setFakeOrdersVersion((v) => v + 1);
        alert("(FAKE) Returned to stock (removed from fake orders).");
        return;
      }
    
      // REAL MODE
    const data = await requestJson("/buyer/unreservebundle/", {
      method: "POST",
      body: {
        reservation_id: order.reservation_id,
      },
    });

    alert("Returned to stock.");

    setBundles((prev) => prev.filter((o) => o.reservation_id !== order.reservation_id));
    setOrdersVersion((v) => v + 1);
  
    } catch (err){
      alert(`Return failed: ${err.message}`);
    }
  }



  return (
    <div className="listings-page">
      <div className="listings-panel" >
        <h2>{isOrders ? "Orders" : "Available Bundles"}</h2>

        {/* toggle: allows you to compare real and fake data */}
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
        

        {/*info dropdown panel */}
        {selectedBundle && (
          <div className="info-panel">
            <div style={{display: "flex", justifyContent: "space-between", gap: 12}}>
              <div>
                <h3 style={{margin: 0}}>{selectedBundle.name ?? "Bundle"}</h3>
                {selectedBundle.price != null && (
                  <p style={{ margin: "6px 0" }}>£{selectedBundle.price}</p>
                )}
              </div>

            <button type="button" onClick={() => setSelectedBundleId(null)}>Close</button>
            </div>

            {selectedBundle.claim_code && (
              <p style={{ margin: "8px 0" }}>
                <strong>Reservation Code:</strong> {selectedBundle.claim_code}
              </p>
            )}

            {selectedBundle.company && (
              <p style={{ margin: "8px 0" }}>
                <strong>Company:</strong> {selectedBundle.company}
              </p>
            )}
            {selectedBundle.collectionLocation && (
              <p style={{ margin: "8px 0" }}>
                <strong>Collection location:</strong> {selectedBundle.collectionLocation}
              </p>
            )}
            {selectedBundle.expiryDate && (
              <p style={{ margin: "8px 0" }}>
                <strong>Expiry date:</strong> {selectedBundle.expiryDate}
              </p>
            )}
            {selectedBundle.allergens && (
              <p style={{ margin: "8px 0" }}>
                <strong>Allergens:</strong>{" "}
                {Array.isArray(selectedBundle.allergens) && selectedBundle.allergens.length > 0
                  ? selectedBundle.allergens.join(", ")
                  : "None listed"}
              </p>
            )}

            {selectedBundle.description && (
              <p style={{ margin: "8px 0" }}>
                <strong>Description:</strong> {selectedBundle.description}
              </p>
            )}
            
            {selectedBundle.created_at && (
              <p style={{ margin: "8px 0" }}>
                <strong>Created:</strong> {new Date(selectedBundle.created_at).toLocaleString()}
              </p>
            )}
          </div>
        )}


        {/* Scrollable list container */}
        <div
          style={{
            maxHeight: 320,          // controls how tall before scrolling
            overflowY: "auto",       // enables scrolling
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
              <h3 style={{ margin: "0 0 6px 0" }}>{bundle.name ?? "Bundle"}</h3>
              {bundle.price != null && (
                <p style={{ margin: "0 0 10px 0" }}>£{bundle.price}</p>
              )}
              {bundle.claim_code && (
                <p style={{ margin: "0 0 10px 0" }}>
                  <strong>Code:</strong> {bundle.claim_code}
                </p>
              )}

              <div style={{ display: "flex", gap: 8, alignItems: "center", flexWrap: "wrap"}}>
                <button
                  type="button"
                  onClick={() => toggleInfo(bundle.id)}
                >
                  {selectedBundleId === bundle.id ? "Hide info" : "Info"}
                </button>
              {isOrders ? (
                <div style={{display: "flex",gap: 8, alignItems: "center", flexWrap: "wrap",}}>
                <span style={{ margin: "0 0 10px 0" }}>
                  <strong>Code:</strong> {bundle.claim_code ?? "—"}
                </span>

                <button onClick={() => returnOrderToStock(bundle)}>
                Return to stock
                </button>
                </div>
              ) : (
                <button onClick={() => redeemBundleCode(bundle.id)}>
                    Redeem code
                </button>
              )}

              </div>
            </div>
          ))}

          {bundlesToShow.length === 0 && !loading && (
            <p style={{ margin: 0 }}>
              {isOrders ? "No orders yet." : "No bundles available."}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
