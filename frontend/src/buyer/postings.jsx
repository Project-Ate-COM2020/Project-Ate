/* --- File Description --- */

/* This file is the buyers marketplace view - they can see all bundles currently being sold */

/* --- Problems and TODOS --- */

// Need to refactor and standardise

// Need to add in some simple search functions

// Potentially connect to google maps API

import { useState } from "react";
import NavBar from "../reusableComponents/navBar.jsx";
import Postings from "../bundlesComponents/postings.jsx";
import Posting from "../bundlesComponents/posting.jsx";
import { useGetData, postData } from "../reusableComponents/api.jsx";
import "./postings.css";

async function reserveBundle(postingID) {
    // For some reason the frontend will now need the ability to generate secure random claim codes - TODO
    if (!postingID) return;
    await postData("marketplace/reservations", { posting: postingID, status: "reserved", "claim_code": "AfFOI" }, true);
}

function UserHomePage(){

    const [selectedPosting, setSelectedPosting] = useState(null);
    const [refreshKey, setRefreshKey] = useState(0);

    const { data, loading } = useGetData("marketplace/bundle/list", { refresh_key: refreshKey }, true);

    const apiBundles = (!loading) ? data.results : [];

    console.log(apiBundles);

    async function handleReserve() {
        const postingID = selectedPosting?.posting ?? selectedPosting?.posting_id;
        if (!postingID) return;
        await reserveBundle(postingID);
        setSelectedPosting(null);
        setRefreshKey((prev) => prev + 1);
    }

    let bundles = [];
    if (!loading) {
        bundles = apiBundles
            .filter((bundle) => Number(bundle?.quantity_remaining ?? 0) > 0)
            .map((bundle) => ({
            posting: bundle.posting ?? bundle.posting_id,
            posting_id: bundle.posting_id ?? bundle.posting,
            bundleName: bundle.contents ?? "Unnamed Bundle",
            bundleCategory: bundle.category ?? "Unknown",
            imgPath: `/${bundle.category}.jpg`,
            pickupTime: bundle.pickup_window ?? "Not specified",
            seller: bundle.seller ? `Seller #${bundle.seller}` : "Unknown seller",
            price: bundle.price ?? "0.00",
            location: bundle.location ?? "Location unavailable",
            stock: bundle.quantity_remaining ?? 0,
        }));
    }

    console.log("bundle list response:", data);

    if (loading) {
        return (
            <div className="buyer-page">
                <NavBar />
                <section className="buyer-hero">
                    <p className="buyer-hero-label">Marketplace</p>
                    <h1 className="buyer-hero-title">Available Bundles</h1>
                    <p className="buyer-hero-subtitle">Loading nearby rescue bundles...</p>
                </section>
                <p className="buyer-postings-loading">Loading postings...</p>
            </div>
        );
    }

    return(
    <div className="buyer-page">
        <NavBar />
        <section className="buyer-hero">
            <p className="buyer-hero-label">Marketplace</p>
            <h1 className="buyer-hero-title">Available Bundles</h1>
            <p className="buyer-hero-subtitle">Browse local rescue bundles and reserve before they are gone.</p>
        </section>
        <section className="buyer-container buyer-postings-content">
            <Postings
                bundles={bundles}
                includedAttributes = {["price", "more info button", "stock", "seller"]}
                numberOfBundles = {bundles.length || 50}
                moreInfoButtonFunction={(bundle) => setSelectedPosting(bundle)}
            />
        </section>

        {selectedPosting && (
            <div className="buyer-modal-overlay" onClick={() => setSelectedPosting(null)}>
                <div className="buyer-modal-content" onClick={(event) => event.stopPropagation()}>
                    <Posting
                        postingData={selectedPosting}
                        includedAttributes={["stock", "pickup time", "location", "price", "seller", "reserve bundle button"]}
                        reserveBundleFunction={handleReserve}
                        backFunction={() => setSelectedPosting(null)}
                    />
                </div>
            </div>
        )}
    </div>
    );

}

export default UserHomePage;