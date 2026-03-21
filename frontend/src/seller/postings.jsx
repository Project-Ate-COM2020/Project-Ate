/* --- Import Statements --- */
import { useState } from "react";
import NavBar from "../reusableComponents/navBar.jsx";
import Postings from "../bundlesComponents/postings.jsx";
import Posting from "../bundlesComponents/posting.jsx";
import { useGetData } from "../reusableComponents/api.jsx";
import "../buyer/buyerShared.css";

/* --- Main Page Function --- */
function SellerPostings() {
    const [selectedPosting, setSelectedPosting] = useState(null);
    const { data, loading } = useGetData("marketplace/bundle/list", {}, true);

    const apiBundles = !loading ? (data?.results ?? []) : [];
    const bundles = apiBundles
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
        allergens: bundle.allergens ?? [],
    }));

    return (
        <div className="buyer-page">
            <NavBar user_type={"seller"} />
            <section className="buyer-hero">
                <p className="buyer-hero-label">Seller Dashboard</p>
                <h1 className="buyer-hero-title">My Postings</h1>
                <p className="buyer-hero-subtitle">Manage and track all your active bundle listings.</p>
            </section>
            <section className="buyer-container buyer-postings-content">
                <Postings
                    bundles={bundles}
                    includedAttributes={["price", "stock", "more info button"]}
                    numberOfBundles={bundles.length || 50}
                    moreInfoButtonFunction={(bundle) => setSelectedPosting(bundle)}
                />
            </section>

            {selectedPosting && (
                <div className="buyer-modal-overlay" onClick={() => setSelectedPosting(null)}>
                    <div className="buyer-modal-content" onClick={(event) => event.stopPropagation()}>
                        <Posting
                            postingData={selectedPosting}
                            includedAttributes={["stock", "pickup time", "location", "price", "allergens"]}
                            backFunction={() => setSelectedPosting(null)}
                        />
                    </div>
                </div>
            )}
        </div>
    );
}

export default SellerPostings;