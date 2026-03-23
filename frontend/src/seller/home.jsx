/* --- File Description --- */
/* Also Following Will's Description to some extent, this file act more as a preview for the seller - allow some small actions to be made - and allow 
the seller to breakout into dedicated pages such as analytics and bundleCreation. 

Includes: 
 - Seller info
 - Analytics
 - Seller Bundle Postings
 - Seller Bundle Reservations
 - Seller Bundle Post Creation + Forecasting
 
each of these will be split up into helper functions for readability and maintainability
*/

/* --- Current Issues --- */

/* The main issue is the current backend bug preventing from loggin in - this means when the backend is fixed 
and endpoints refactored, the endpoints and maybe the parsing for this file will also need to change */

/* --- Import Statements --- */
import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import NavBar from "../reusableComponents/navBar.jsx";
import Postings from "../bundlesComponents/postings.jsx";
import ReservedBundles from "../bundlesComponents/bundles.jsx";
import { useGetData, getData } from "../reusableComponents/api.jsx";
import "./home.css";

/* --- Helper Functions --- */

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

function Analytics() {
    const navigate = useNavigate();
    const sellerId = localStorage.getItem("seller_id") || localStorage.getItem("sellerId") || "1";
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);

    function toSafeNumber(value, fallback = 0) {
        if (typeof value === "number") {
            return Number.isFinite(value) ? value : fallback;
        }
        if (typeof value === "string") {
            const parsed = Number(value);
            return Number.isFinite(parsed) ? parsed : fallback;
        }
        return fallback;
    }

    useEffect(() => {
        async function fetchStats() {
            try {
                const params = { seller_id: sellerId };
                const [listings, revenue, collection] = await Promise.all([
                    getData('analytics/total-listings/', params, true),
                    getData('analytics/total-revenue/', params, true),
                    getData('analytics/food-waste-reduction/', params, true),
                ]);
                setStats({
                    listings: toSafeNumber(listings, 0),
                    revenue: toSafeNumber(revenue, 0),
                    collection: toSafeNumber(collection?.food_waste_reduction_percentage, 0),
                });
            } catch (err) {
                console.error('Failed to fetch analytics:', err);
            } finally {
                setLoading(false);
            }
        }
        fetchStats();
    }, [sellerId]);

    const displayListings = loading ? "Loading..." : stats?.listings;
    const displayRevenue = loading ? "Loading..." : (stats?.revenue ? `£${Number(stats.revenue).toFixed(2)}` : "£0.00");
    const displayCollection = loading ? "Loading..." : `${stats?.collection ?? 0}%`;

    return (
        <div className = "analytics">

            <h4>Analytics</h4>

            <button className = "button" onClick={() => navigate("/seller/analytics")}>View All Analytics</button>

            <div className = "infoContainer">

                <div className = "info">
                    <p>Total Number of Listings: {displayListings}</p>
                </div>

                <div className = "info">
                    <p>Total Revenue: {displayRevenue}</p>
                </div>

                <div className = "info">
                    <p>Collection Rate: {displayCollection}</p>
                </div>

            </div>
        </div>
    )
}

function BundlePostings() {
    const navigate = useNavigate();
    const { data, loading } = useGetData("marketplace/bundle/list", {}, true);

    const apiBundles = !loading ? (data?.results ?? []) : [];
    const bundles = apiBundles
        .filter((bundle) => Number(bundle?.quantity_remaining ?? 0) > 0)
        .map((bundle) => ({
        posting: bundle.posting ?? bundle.posting_id,
        posting_id: bundle.posting_id ?? bundle.posting,
        bundleName: bundle.contents ?? "Unnamed Bundle",
        bundleCategory: formatCategoryLabel(bundle.category),
        imgPath: getImagePathFromCategory(bundle.category),
        pickupTime: bundle.pickup_window ?? "Not specified",
        seller: bundle.seller ? `Seller #${bundle.seller}` : "Unknown seller",
        price: bundle.price ?? "0.00",
        location: bundle.location ?? "Location unavailable",
        stock: bundle.quantity_remaining ?? 0,
        allergens: bundle.allergens ?? [],
    }));

    return (
        <div className = "dashboardPanel bundlePostings">
            <h4>Bundle Postings</h4>
            <button className = "button" onClick={() => navigate("/seller/createPosting")}>Create New Posting</button>
            <button className = "button" onClick={() => navigate("/seller/postings")}>View All Postings</button>
            <Postings
                bundles={bundles}
                includedAttributes = {["price", "stock", "more info button"]}
                numberOfBundles={3}
                moreInfoButtonFunction={(bundle) => navigate("/seller/postings", { state: { postingData: bundle } })}
            />
        </div>
    )
}

function BundleReservations() {
    const navigate = useNavigate();
    const { data } = useGetData("marketplace/reservations/list", {}, true);
    const apiReservations = Array.isArray(data)
        ? data
        : Array.isArray(data?.results)
            ? data.results
            : [];

    const reservations = apiReservations
        .filter((reservation) => {
            const status = String(reservation?.status ?? "").toLowerCase();
            return status === "reserved" || status === "active";
        })
        .map((reservation) => ({
        reservation_id: reservation.reservation_id,
        posting: reservation.posting,
        consumer: reservation.consumer,
        timestamp: reservation.timestamp,
        claim_code: reservation.claim_code,
        status: reservation.status,
        no_show_reason: reservation.no_show_reason,
        collected_at: reservation.collected_at,
        bundleName: reservation.contents ?? `Reservation #${reservation.reservation_id}`,
        bundleCategory: formatCategoryLabel(reservation.bundleCategory),
        imgPath: getImagePathFromCategory(reservation.bundleCategory),
        pickupTime: formatPickupTime(reservation.timestamp),
        seller: reservation.posting ? `Posting #${reservation.posting}` : "Unknown",
        buyer: reservation.consumerDisplayName || "Unknown",
        collectionCode: reservation.claim_code ?? "N/A",
        price: reservation.price ?? "N/A",
        location: reservation.location ?? "Location unavailable",
    }));

    return (
        <div className = "dashboardPanel bundleReservations">
            <h4>Customer Reservations</h4>
            <button className = "button" onClick={() => navigate("/seller/reservations")}>View All Reservations</button>
            <ReservedBundles
                bundles={reservations}
                includedAttributes = {["buyer", "pickup time", "more info button"]}
                numberOfBundles={3}
                moreInfoButtonFunction={(bundle) => navigate("/seller/reservations", { state: { reservationData: bundle } })}
            />
        </div>
    )
}

/* --- Main Page Function --- */

function SellerHomePage() {
    return (
        <div className = "buyer-page sellerHomePage">
            <NavBar user_type = "seller"/>
            <section className="buyer-hero">
                <p className="buyer-hero-label">Dashboard</p>
                <h1 className="buyer-hero-title">Seller Home</h1>
                <p className="buyer-hero-subtitle">Quick overview of your listings, reservations, and performance.</p>
            </section>
            <div className = "buyer-container dashboardGrid">
                <Analytics />
                <BundlePostings />
                <BundleReservations />
            </div>
        </div>
    )

}

export default SellerHomePage;