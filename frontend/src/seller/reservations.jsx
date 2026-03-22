/* --- Import Functions --- */
import { useState } from "react";
import NavBar from "../reusableComponents/navBar.jsx";
import Bundles from "../bundlesComponents/bundles.jsx";
import Bundle from "../bundlesComponents/bundle.jsx";
import { useGetData, putData } from "../reusableComponents/api.jsx";
import "../buyer/buyerShared.css";
import "../buyer/reservations.css";

/* --- Main Page Function --- */
function SellerReservations() {
    const [selectedReservation, setSelectedReservation] = useState(null);
    const [refreshKey, setRefreshKey] = useState(0);

    const { data } = useGetData("marketplace/reservations/list", { refresh_key: refreshKey }, true);
    const apiReservations = Array.isArray(data)
        ? data
        : (Array.isArray(data?.results) ? data.results : []);

    async function markCollected() {
        if (!selectedReservation?.reservation_id) return;

        await putData(
            `marketplace/reservations/${selectedReservation.reservation_id}/`,
            {
                posting: selectedReservation.posting,
                consumer: selectedReservation.consumer,
                claim_code: selectedReservation.claim_code,
                status: "collected",
                timestamp: selectedReservation.timestamp,
                no_show_reason: selectedReservation.no_show_reason,
                collected_at: new Date().toISOString(),
            },
            true,
        );

        setSelectedReservation(null);
        setRefreshKey((prev) => prev + 1);
    }

    const visibleReservations = apiReservations
        .filter((reservation) => {
            const status = String(reservation?.status ?? "").toLowerCase();
            return status === "reserved" || status === "active";
        });

    const reservations = visibleReservations
        .map((reservation) => ({
        reservation_id: reservation.reservation_id,
        posting: reservation.posting,
        consumer: reservation.consumer,
        timestamp: reservation.timestamp,
        claim_code: reservation.claim_code,
        status: reservation.status,
        no_show_reason: reservation.no_show_reason,
        collected_at: reservation.collected_at,
        bundleName: reservation.contents ?? `Posting #${reservation.posting}`,
        bundleCategory: reservation.bundleCategory ?? "Reserved bundle",
        imgPath: `/${reservation.bundleCategory ?? "Dairy"}.jpg`,
        pickupTime: reservation.timestamp ?? "Not specified",
        seller: reservation.posting ? `Posting #${reservation.posting}` : "Unknown",
        buyer: reservation.consumer ? `Consumer #${reservation.consumer}` : "Unknown",
        collectionCode: reservation.claim_code ?? "N/A",
        price: reservation.price ?? "N/A",
        location: reservation.location ?? "Location unavailable",
    }));

    console.log("[SellerReservations] API payload:", data);
    console.log("[SellerReservations] apiReservations count:", apiReservations.length);
    console.log(
        "[SellerReservations] statuses:",
        apiReservations.map((reservation) => reservation?.status)
    );
    console.log("[SellerReservations] visibleReservations count:", visibleReservations.length);
    console.log("[SellerReservations] mapped reservations:", reservations);

    return (
        <div className="buyer-page buyer-reservations-page">
            <NavBar user_type={"seller"} />
            <section className="buyer-hero buyer-reservations-hero">
                <p className="buyer-hero-label">Seller Dashboard</p>
                <h1 className="buyer-hero-title">Customer Reservations</h1>
                <p className="buyer-hero-subtitle">Track active customer reservations and collection statuses.</p>
            </section>
            <section className="buyer-container buyer-reservations-content">
                <Bundles
                    bundles={reservations}
                    includedAttributes={["buyer", "pickup time", "more info button"]}
                    numberOfBundles={reservations.length || 50}
                    moreInfoButtonFunction={(bundle) => setSelectedReservation(bundle)}
                />
            </section>

            {selectedReservation && (
                <div className="buyer-modal-overlay" onClick={() => setSelectedReservation(null)}>
                    <div className="buyer-modal-content" onClick={(event) => event.stopPropagation()}>
                        <Bundle
                            bundleData={selectedReservation}
                            includedAttributes={["buyer", "pickup time", "mark collected button", "collection code"]}
                            markCollectedFunction={markCollected}
                            backfunction={() => setSelectedReservation(null)}
                        />
                    </div>
                </div>
            )}
        </div>
    );
}

export default SellerReservations;