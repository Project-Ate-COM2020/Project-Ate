/* Lists all the available bundle postings to the user */

import "./Listings.css";                               /*css link */
import { login, getAccessToken } from "../api/auth";   /*Allows authentication on the website to be stored locally*/
import fakeBundles from "./fakeBundles";               /*faked data for frontend testing without the backend*/
import { addFakeOrder, makeClaimCode, getFakeOrders, removeFakeOrder } from "./fakeOrdersStore" /* more fake utilies for the backend*/
import { useEffect, useMemo, useState } from "react";  /* It imports the different react hooks  */
import {
  fetchMarketplaceBundles,
  fetchMarketplaceOrders,
  createReservationForPosting,
  API_BASE
} from "../api/marketplace"; /* imports all the key API functions the listing and order page needs*/




// Automatically assumes the state is listings unless metioned elsewhere 
export default function Listings({ mode = "listings" }) {

  const isOrders = mode === "orders"; /*changes the mode when on the /orders page*/

  const [bundles, setBundles] = useState([]);        /* Stores the real data from the backend*/ 
  const [loading, setLoading] = useState(true);      /* It accounts for Loading while the async function runs*/ 

  // manual toggle for fake and real data for testing purposes 
  const [useFake, setUseFake] = useState(false); 

  // This is the Fall back if the API fails 
  const [apiFailed, setApiFailed] = useState(false); 

  // stores which bundle has been selected for the info button to appear 
  const [selectedBundleId, setSelectedBundleId] = useState(null);

  // version counters forcing react to upadate when the remove button is pressed 
  const [fakeOrdersVersion, setFakeOrdersVersion] = useState(0);
  const [ordersVersion, setOrdersVersion] = useState(0)

  

// This a an async function that loads the bundles whilst the rest of the page loads 
// and loads the bundles whilst the rest of the page loads
useEffect(() => {

  async function loadBundles() {
    try {
      setLoading(true);          // shows loading message on screen
      setApiFailed(false);       // resets API failure state

      // **************************************************
      // First logs in as a test user so the backend
      // recognises the request as authenticated
      if (!getAccessToken()) {
        await login("will", "will"); // can change to any known login for testing
      }

      // **************************************************
      // Fetches either the orders or bundles depending
      // on which mode the component is currently in
      let data;
      let bundlesList = null;
      
      if (isOrders) {
        data = await fetchMarketplaceOrders();        // reservations
        bundlesList = await fetchMarketplaceBundles(); // postings to be able to look them up
      } else {
        data = await fetchMarketplaceBundles();       // postings
      }

      console.log("raw API data:", data);  // allows debugging in browser console


      // **************************************************
      // Normalises backend data so it matches the format
      // expected by the frontend UI
      const normalised = isOrders
      ? data.map((r) => {  //reservations on the order page getting normilised 

          const postingIdRaw =
            r.bundle ?? r.posting ?? r.bundle_id ?? r.posting_id;    

          const postingId = postingIdRaw != null ? Number(postingIdRaw) : null;

          const realReservationId = r.id ?? r.reservation_id ?? null; 

          // creates 3 fall back keys to make sure there is a Unique / stable key for each item in the list
          const reactKey = 
            realReservationId ?? `${postingIdRaw}-${r.claim_code ?? Math.random()}`;

          // manually joins the 2 different DB together so all the information can be dsiplayed  
          const posting = Array.isArray(bundlesList)
            ? bundlesList.find((p) => Number(p.posting_id) === postingId)
            : null;
            // all the information that can be displayed on the orders page 
            return {
              key: reactKey,
              id: realReservationId,  
              claim_code: r.claim_code,
              status: r.status,
              created_at: r.created_at,
              posting_id: postingId,  
              name: posting ? `${posting.category} bundle` : `Bundle ${postingId ?? "—"}`,
              price: posting?.price ?? "—", // "-" keeps the UI readable if no data is there 
              company: "—",
              collectionLocation: "—",
              expiryDate: posting?.pickup_window ?? "—", 
              allergens: posting?.allergens ?? [],
              description: posting?.contents ?? "",
            };
        })
      : data.map((p) => { //posting  the avablie bundles to the user on the order page 
          
          console.log("RAW POSTING OBJECT:", p);

          return {
            id: p.posting_id,
            posting_id: p.posting_id,
            bundle_id: p.bundle_id ?? p.bundle ?? null,
            name: `${p.category} bundle`,
            price: p.price,
            company: "—",
            collectionLocation: "—",
            expiryDate: p.pickup_window,
            allergens: p.allergens,
            description: p.contents,
          };
        });
        
        // decided whether the API failed or sucseeded based off if the info was nomilised 
        if (!Array.isArray(normalised)) { 
          setApiFailed(true);
          setBundles([]);
        } else {
          setApiFailed(false);
          setBundles(normalised);
        }

    } catch (err) {
      console.error("Failed to load bundles:", err);
      setApiFailed(true);         // triggers fallback mode
      setBundles([]);
    } finally {
      setLoading(false);          // removes loading message
    }
  }

  loadBundles();   // runs the async function when component loads

}, [isOrders, ordersVersion]);  // re-runs when mode or orders change


  // updates the react components when the variables in the [] change on the webpage 
  const bundlesToShow = useMemo(() => {
    if (isOrders) {
      if (useFake) return getFakeOrders();
      if (apiFailed) return getFakeOrders();   // fallback
      return bundles;
    }
  
    if (useFake || apiFailed) return fakeBundles;
    return bundles;
  }, [isOrders, useFake, apiFailed, bundles,fakeOrdersVersion,]);

  // find the selected bundle object so the info data is correct for it 
  const selectedBundle = useMemo(() => {
    if (selectedBundleId == null) return null;
    return bundlesToShow.find((b) => b.id === selectedBundleId) || null;
  }, [selectedBundleId, bundlesToShow]);


  // POST OP to redeem code

  async function redeemBundleCode(bundleId) {
    try {
      const bundle = bundlesToShow.find((b) => b.id === bundleId);
      if (!bundle) {
        alert("Bundle not found");
        return;
      }
  
      // FAKE MODE
      if (useFake || apiFailed) {
        const claim = makeClaimCode();
  
        addFakeOrder({
          order_id: Date.now(),
          claim_code: claim,
          status: "RESERVED",
          created_at: new Date().toISOString(),
          ...bundle,
        });
  
        alert(`(FAKE) Order created!\nCode: ${claim}`);
        return;
      }
  
      // REAL MODE (backend)
      const consumerId = 1; // ********************* change to the customer once the login system works 

      const postingPk = bundle.id; // extracts the ID of the posing selected 
      if (!postingPk) {
        alert("Backend did not provide the posting PK (id).");
        return;
      }

      const postingId = bundle.posting_id ?? bundle.id; // connects the correct ID as it handles real and fake data 

      // sends the nessary info to the backend for the backend to return the bundle code and status change 
      const created = await createReservationForPosting(postingId, consumerId); 
      
      alert(`Reserved! Code: ${created.claim_code}`);
      setOrdersVersion((v) => v + 1);
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
  try {
    if (!order) return;

    // FAKE MODE
    if (useFake || apiFailed) {
      if (order.order_id == null) {
        alert("Can't remove fake order: missing order_id");
        return;
      }
      removeFakeOrder(order.order_id);
      setFakeOrdersVersion((v) => v + 1);
      alert("(FAKE) Returned to stock (removed from fake orders).");
      return;
    }

    // REAL MODE (backend) — delete reservation
    const token = getAccessToken();

    const reservationId = order.id; 

    if (!reservationId) {
      alert("Can't return to stock: backend didn't send reservation id.");
      return;
    }


    const res = await fetch(`${API_BASE}/marketplace/reservations/${reservationId}/`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      credentials: "omit",
    });

    if (!res.ok) {
      const text = await res.text();
      throw new Error(text || `HTTP ${res.status}`);
    }

    alert("Returned to stock.");

    // Remove from UI
    setBundles((prev) => prev.filter((o) => o.id !== reservationId));

    setOrdersVersion((v) => v + 1);
  } catch (err) {
    alert(`Return failed: ${err.message}`);
  }
}

return (
    <div className="listings-page">
      <div className="listings-panel">
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
            <span style={{ fontSize: 12 }}>API unavailable/empty → showing fake bundles</span>
          )}

          {!loading && !apiFailed && !useFake && (
            <span style={{ fontSize: 12 }}>Showing API bundles</span>
          )}
        </div>

        {/* Scrollable list container */}
        <div
          style={{
            maxHeight: 320,
            overflowY: "auto",
            border: "1px solid #ddd",
            borderRadius: 8,
            padding: 12,
          }}
        >
          {bundlesToShow.slice(0, 20).map((bundle) => {
            const isOpen = selectedBundleId === bundle.id;

            return (
              <div
                key={bundle.key ?? bundle.id}
                style={{
                  borderBottom: "1px solid #eee",
                  padding: "12px 0",
                }}
              >
                <h3 style={{ margin: "0 0 6px 0" }}>{bundle.name}</h3>
                <p style={{ margin: "0 0 10px 0" }}>£{bundle.price}</p>

                <div className="bundle-actions">
                  <button type="button" onClick={() => toggleInfo(bundle.id)}>
                    {isOpen ? "Hide info" : "Info"}
                  </button>

                  {isOrders ? (
                    <>
                      <div className="order-meta">
                        <span>
                          <strong>Code:</strong> {bundle.claim_code ?? "—"}
                        </span>
                        <span>
                          <strong>Status:</strong> {bundle.status ?? "—"}
                        </span>
                      </div>

                      <button type="button" onClick={() => returnOrderToStock(bundle)}>
                        Return to stock
                      </button>
                    </>
                  ) : (
                    <button type="button" onClick={() => redeemBundleCode(bundle.id)}>
                      Redeem code
                    </button>
                  )}
                </div>

                {/* INFO PANNEL inside the scrollable list  */}
                {isOpen && (
                  <div className="info-panel" style={{ marginTop: 10 }}>
                    <div style={{ display: "flex", justifyContent: "space-between", gap: 12 }}>
                      <div>
                        <h3 style={{ margin: 0 }}>{bundle.name}</h3>
                        <p style={{ margin: "6px 0" }}>£{bundle.price}</p>
                      </div>

                      <button type="button" onClick={() => setSelectedBundleId(null)}>
                        Close
                      </button>
                    </div>

                    <p style={{ margin: "8px 0" }}>
                      <strong>Company:</strong> {bundle.company ?? "—"}
                    </p>
                    <p style={{ margin: "8px 0" }}>
                      <strong>Collection location:</strong> {bundle.collectionLocation ?? "—"}
                    </p>
                    <p style={{ margin: "8px 0" }}>
                      <strong>Expiry date:</strong> {bundle.expiryDate ?? "—"}
                    </p>
                    <p style={{ margin: "8px 0" }}>
                      <strong>Allergens:</strong>{" "}
                      {Array.isArray(bundle.allergens) && bundle.allergens.length > 0
                        ? bundle.allergens.join(", ")
                        : "None listed"}
                    </p>

                    {bundle.description && (
                      <p style={{ margin: "8px 0" }}>
                        <strong>Description:</strong> {bundle.description}
                      </p>
                    )}
                  </div>
                )}
              </div>
            );
          })}

          {bundlesToShow.length === 0 && !loading && (
            <p style={{ margin: 0 }}>{isOrders ? "No orders yet." : "No bundles available."}</p>
          )}
        </div>
      </div>
    </div>
  );
}
