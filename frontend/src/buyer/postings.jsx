/* --- File Description --- */

/* This file is the buyers marketplace view - they can see all bundles currently being sold */

/* --- Problems and TODOS --- */

// Need to refactor and standardise

// Need to add in some simple search functions

// Potentially connect to google maps API

import { useState } from "react";
import { customAlphabet } from "nanoid";
import NavBar from "../reusableComponents/navBar.jsx";
import Postings from "../bundlesComponents/postings.jsx";
import Posting from "../bundlesComponents/posting.jsx";
import { useGetData, postData } from "../reusableComponents/api.jsx";
import "./postings.css";

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

const generateClaimCode = customAlphabet("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890", 7);

async function reserveBundle(postingID) {
    if (!postingID) return;
    await postData("marketplace/reservations", { posting: postingID, status: "reserved", "claim_code": generateClaimCode() }, true);
}

function UserHomePage(){

    const [selectedPosting, setSelectedPosting] = useState(null);
    const [refreshKey, setRefreshKey] = useState(0);
    const [selectedLocation, setSelectedLocation] = useState("all");
    const [selectedCategory, setSelectedCategory] = useState("all");

    const { data, loading } = useGetData("marketplace/bundle/list", { refresh_key: refreshKey }, true);

    const apiBundles = Array.isArray(data?.results) ? data.results : [];

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
            bundleCategory: formatCategoryLabel(bundle.category),
            imgPath: getImagePathFromCategory(bundle.category),
            pickupTime: bundle.pickup_window ?? "Not specified",
            seller: bundle.seller ? `Seller #${bundle.seller}` : "Unknown seller",
            price: bundle.price ?? "0.00",
            location: bundle.sellerLocation || "Location unavailable",
            stock: bundle.quantity_remaining ?? 0,
            allergens: bundle.allergens ?? [],
        }));
    }

    const locationOptions = [...new Set(bundles.map((bundle) => bundle.location))]
        .filter((location) => Boolean(location))
        .sort((a, b) => a.localeCompare(b));

    const categoryOptions = [...new Set(bundles.map((bundle) => bundle.bundleCategory))]
        .filter((category) => Boolean(category))
        .sort((a, b) => a.localeCompare(b));

    const filteredBundles = bundles.filter((bundle) => {
        const locationMatches = selectedLocation === "all" || bundle.location === selectedLocation;
        const categoryMatches = selectedCategory === "all" || bundle.bundleCategory === selectedCategory;
        return locationMatches && categoryMatches;
    });

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
            <div className="buyer-postings-filters">
                <div className="buyer-postings-filter-row">
                    <label className="buyer-postings-filter-label" htmlFor="bundle-location-filter">
                        Filter by location
                    </label>
                    <select
                        id="bundle-location-filter"
                        className="buyer-postings-filter-select"
                        value={selectedLocation}
                        onChange={(event) => setSelectedLocation(event.target.value)}
                    >
                        <option value="all">All locations</option>
                        {locationOptions.map((location) => (
                            <option key={location} value={location}>
                                {location}
                            </option>
                        ))}
                    </select>
                </div>
                <div className="buyer-postings-filter-row">
                    <label className="buyer-postings-filter-label" htmlFor="bundle-category-filter">
                        Filter by category
                    </label>
                    <select
                        id="bundle-category-filter"
                        className="buyer-postings-filter-select"
                        value={selectedCategory}
                        onChange={(event) => setSelectedCategory(event.target.value)}
                    >
                        <option value="all">All categories</option>
                        {categoryOptions.map((category) => (
                            <option key={category} value={category}>
                                {category}
                            </option>
                        ))}
                    </select>
                </div>
            </div>
            <Postings
                bundles={filteredBundles}
                includedAttributes = {["price", "more info button", "stock", "seller"]}
                numberOfBundles = {filteredBundles.length || 50}
                moreInfoButtonFunction={(bundle) => setSelectedPosting(bundle)}
            />
        </section>

        {selectedPosting && (
            <div className="buyer-modal-overlay" onClick={() => setSelectedPosting(null)}>
                <div className="buyer-modal-content" onClick={(event) => event.stopPropagation()}>
                    <Posting
                        postingData={selectedPosting}
                        includedAttributes={["stock", "pickup time", "location", "price", "seller", "allergens", "reserve bundle button"]}
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