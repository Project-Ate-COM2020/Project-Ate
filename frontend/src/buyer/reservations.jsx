/* --- File Description --- */

/* This is the reservations page - where a user can view their reserved bundles, the location and has the option to unreserve */

/* --- Current Problems and TODOS --- */

// Need to comment and refactor and standardise

// Need to add in function to generate a random claim code securely

// Potentially connect to google maps API

/* --- Import Statements --- */
import { useState } from "react";
import NavBar from "../reusableComponents/navBar.jsx";
import Bundles from "../bundlesComponents/bundles.jsx";
import Bundle from "../bundlesComponents/bundle.jsx";
import { useGetData, deleteData } from "../reusableComponents/api.jsx";
import "./reservations.css";

const CATEGORY_IMAGE_PATHS = {
  bakery: "/bakery.jpg",
  dairy: "/dairy.jpg",
  desserts: "/desserts.jpg",
  fresh_produce: "/fresh produce.jpg",
  hot_meals: "/hot meals.jpg",
  prepared_salads: "/prepared salads.jpg",
};

function getImagePathFromCategory(category) {
  return CATEGORY_IMAGE_PATHS[String(category || "").toLowerCase()] || "/dairy.jpg";
}

function formatCategoryLabel(category) {
  return String(category || "dairy")
    .replace(/_/g, " ")
    .replace(/\b\w/g, (ch) => ch.toUpperCase());
}

function formatPickupTime(timestamp) {
  if (!timestamp) return "Not specified";

  const parsed = new Date(timestamp);
  if (Number.isNaN(parsed.getTime())) return "Not specified";

  return parsed.toLocaleString(undefined, {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

/* --- Helper Functions --- */
async function unreserveBundle(reservationID) {
  await deleteData(`marketplace/reservations/${reservationID}/`, true);
}

/* --- Main Function --- */
function Reservations() {
  
  // Modal indicator and refresh key for automatic refresh when info sent
  const [selectedReservation, setSelectedReservation] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);


  // Defining the api reservations using a hook for automatic updates (utilises refresh key)
  const { data, loading } = useGetData("marketplace/reservations/list", { refresh_key: refreshKey }, true);

  const apiReservations = Array.isArray(data)
    ? data
    : (Array.isArray(data?.results) ? data.results : []);

  // function handling the unreserve of a bundle - then refreshes using refresh key
  async function handleUnreserve() {
    await unreserveBundle(selectedReservation.reservation_id);
    setSelectedReservation(null);
    setRefreshKey((prev) => prev + 1);
  }

  // Safe handling of reservations before specific are nailed down later
  let reservations = [];
  if (!loading) {
  reservations = apiReservations
    .filter((reservation) => {
      const status = String(reservation?.status ?? "").toLowerCase();
      return status === "reserved";
    })
    .map((reservation) => ({
    reservation_id: reservation.reservation_id,
    posting: reservation.posting,
    bundleName: reservation.contents ?? `Reservation #${reservation.reservation_id}`,
    bundleCategory: formatCategoryLabel(reservation.bundleCategory),
    imgPath: getImagePathFromCategory(reservation.bundleCategory),
    pickupTime: reservation.pickupWindow || "Not specified",
    seller: reservation.sellerName || (reservation.sellerId ? `Seller #${reservation.sellerId}` : "Unknown"),
    buyer: reservation.consumerDisplayName || "Unknown",
    collectionCode: reservation.claim_code ?? "N/A",
    price: reservation.price ?? "N/A",
    location: reservation.sellerLocation || "Location unavailable",
  }));
  }

    // loading screen defined
    if (loading) {
        return (
        <div className="buyer-page buyer-reservations-page">
                <NavBar />
          <section className="buyer-hero buyer-reservations-hero">
            <p className="buyer-hero-label buyer-reservations-label">Your Orders</p>
            <h1 className="buyer-hero-title buyer-reservations-title">My Reservations</h1>
            <p className="buyer-hero-subtitle buyer-reservations-subtitle">Loading your latest reservation details...</p>
          </section>
            </div>
        );
    }

    // React Component
    return (
      <div className="buyer-page buyer-reservations-page">
        <NavBar />
        <section className="buyer-hero buyer-reservations-hero">
          <p className="buyer-hero-label buyer-reservations-label">Your Orders</p>
          <h1 className="buyer-hero-title buyer-reservations-title">My Reservations</h1>
          <p className="buyer-hero-subtitle buyer-reservations-subtitle">
            Keep track of collection windows, claim codes and pickup locations in one place.
          </p>
        </section>

        <section className="buyer-container buyer-reservations-content">
          <Bundles
            bundles={reservations}
            includedAttributes = {["more info button", "Pickup time", "collection code"]}
            numberOfBundles = {reservations.length || 50}
            moreInfoButtonFunction={(bundle) => setSelectedReservation(bundle)}
          />
        </section>
        {/* Shows modal if toggle is on */}
        {selectedReservation && (
          <div className="buyer-modal-overlay" onClick={() => setSelectedReservation(null)}>
            <div className="buyer-modal-content" onClick={(event) => event.stopPropagation()}>
              <Bundle
                bundleData={selectedReservation}
                includedAttributes={["Pickup time", "collection code", "seller", "location", "unreserve bundle button"]}
                unreserveBundleFunction={handleUnreserve}
                backfunction={() => setSelectedReservation(null)}
              />
            </div>
          </div>
        )}
      </div>
    );
  }

/* --- Export Page Function --- */
export default Reservations;