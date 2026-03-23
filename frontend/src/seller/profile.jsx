/* --- Import Statements --- */
import { useCallback, useEffect, useState } from "react";
import { jwtDecode } from "jwt-decode";
import { useNavigate } from "react-router-dom";
import NavBar from "../reusableComponents/navBar.jsx";
import { getData, putData } from "../reusableComponents/api.jsx";
import "./profile.css";

/* --- Helper Functions --- */
function formatDate(isoString) {
    if (!isoString) return "N/A";
    return new Date(isoString).toLocaleDateString(undefined, {
        day: "numeric",
        month: "short",
        year: "numeric",
    });
}

function getSellerIdFromToken() {
    const token = localStorage.getItem("access_token");
    if (!token) return null;

    try {
        const payload = jwtDecode(token);
        return payload?.seller_id ?? null;
    } catch {
        return null;
    }
}

function mapSellerApiToState(seller) {
    return {
        sellerId: seller?.seller_id ?? null,
        sellerName: seller?.name ?? "",
        accountLifetime: formatDate(seller?.created_at),
        location: seller?.location ?? "",
        openingHours: seller?.opening_hours ?? "",
        contactStub: seller?.contact_stub ?? "",
        createdAt: seller?.created_at ?? null,
    };
}

/* --- Main Page Function --- */
function SellerProfilePage() {
    const navigate = useNavigate();
    const [editMode, setEditMode] = useState(false);
    const [sellerInfo, setSellerInfo] = useState(null);
    const [formValues, setFormValues] = useState({
        sellerName: "",
        location: "",
        openingHours: "",
        contactStub: "",
    });
    const [isSaving, setIsSaving] = useState(false);
    const [error, setError] = useState(null);

    const handleLogout = useCallback(() => {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("user_type");
        localStorage.removeItem("seller_id");
        localStorage.removeItem("sellerId");
        navigate("/login");
    }, [navigate]);

    const loadSellerProfile = useCallback(async () => {
        setError(null);

        let sellerId = getSellerIdFromToken() || localStorage.getItem("seller_id") || localStorage.getItem("sellerId");

        if (!sellerId) {
            const listResponse = await getData("marketplace/seller/list", {}, true);
            if (Array.isArray(listResponse) && listResponse.length > 0) {
                sellerId = listResponse[0]?.seller_id;
            }
        }

        if (!sellerId) {
            setError("Could not determine seller account. Please log in again.");
            return;
        }

        const response = await getData(`marketplace/seller/${sellerId}/`, {}, true);

        if (!response || !response.seller_id) {
            const detail = typeof response?.detail === "string" ? response.detail : "Failed to load seller profile.";
            setError(detail);
            return;
        }

        localStorage.setItem("seller_id", String(response.seller_id));

        const mapped = mapSellerApiToState(response);
        setSellerInfo(mapped);
        setFormValues({
            sellerName: mapped.sellerName,
            location: mapped.location,
            openingHours: mapped.openingHours,
            contactStub: mapped.contactStub,
        });
    }, []);

    useEffect(() => {
        loadSellerProfile();
    }, [loadSellerProfile]);

    const handleEdit = () => {
        if (!sellerInfo) return;

        setFormValues({
            sellerName: sellerInfo.sellerName,
            location: sellerInfo.location,
            openingHours: sellerInfo.openingHours,
            contactStub: sellerInfo.contactStub,
        });
        setEditMode(true);
    };

    const handleCancel = () => {
        if (!sellerInfo) return;

        setFormValues({
            sellerName: sellerInfo.sellerName,
            location: sellerInfo.location,
            openingHours: sellerInfo.openingHours,
            contactStub: sellerInfo.contactStub,
        });
        setEditMode(false);
    };

    const handleSave = async () => {
        if (!sellerInfo?.sellerId || isSaving) return;

        setIsSaving(true);
        setError(null);

        const payload = {
            name: formValues.sellerName,
            location: formValues.location,
            opening_hours: formValues.openingHours,
            contact_stub: formValues.contactStub,
        };

        const response = await putData(`marketplace/seller/${sellerInfo.sellerId}/`, payload, true);

        if (!response || !response.seller_id) {
            const detail = typeof response?.detail === "string" ? response.detail : "Could not save profile changes.";
            setError(detail);
            setIsSaving(false);
            return;
        }

        const mapped = mapSellerApiToState(response);
        setSellerInfo(mapped);
        setFormValues({
            sellerName: mapped.sellerName,
            location: mapped.location,
            openingHours: mapped.openingHours,
            contactStub: mapped.contactStub,
        });
        setEditMode(false);
        setIsSaving(false);
    };

    const handleChange = (field) => (event) => {
        setFormValues((prev) => ({ ...prev, [field]: event.target.value }));
    };

    if (error && !sellerInfo) {
        return (
            <div className="buyer-page profile-page seller-profile-page">
                <NavBar />
                <div className="buyer-container profile-state">
                    <div className="profile-error">
                        <h2>Seller profile</h2>
                        <p>{error}</p>
                        <button className="profile-btn-ghost" type="button" onClick={loadSellerProfile}>
                            Try again
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    if (!sellerInfo) {
        return (
            <div className="buyer-page profile-page seller-profile-page">
                <NavBar />
                <div className="buyer-container profile-state">
                    <p className="profile-loading">Loading…</p>
                </div>
            </div>
        );
    }

    const firstLetter = sellerInfo.sellerName ? sellerInfo.sellerName[0].toUpperCase() : "?";

    return (
        <div className="buyer-page profile-page seller-profile-page">
            <NavBar />

            <section className="buyer-hero profile-banner">
                <div className="buyer-container profile-banner-inner">
                    <div className="profile-avatar">{firstLetter}</div>

                    <div className="profile-identity">
                        <h1 className="profile-name">{sellerInfo.sellerName || "Unknown Seller"}</h1>
                    </div>

                    <div className="profile-actions">
                        {!editMode ? (
                            <>
                                <button className="profile-btn-ghost profile-btn-ghost--light" type="button" onClick={handleEdit}>
                                    Edit profile
                                </button>
                                <button className="profile-btn-ghost profile-btn-ghost--light" type="button" onClick={handleLogout}>
                                    Log out
                                </button>
                            </>
                        ) : (
                            <>
                                <button
                                    className="profile-btn-ghost profile-btn-ghost--light"
                                    type="button"
                                    onClick={handleSave}
                                    disabled={isSaving}
                                >
                                    {isSaving ? "Saving..." : "Save changes"}
                                </button>
                                <button
                                    className="profile-btn-ghost profile-btn-ghost--light"
                                    type="button"
                                    onClick={handleCancel}
                                    disabled={isSaving}
                                >
                                    Cancel
                                </button>
                            </>
                        )}
                    </div>
                </div>
            </section>

            <div className="buyer-container profile-wrap">
                {error && <p className="profile-empty">{error}</p>}

                <div className="profile-stats-row">
                    <div className="profile-stat">
                        <span className="profile-stat-number profile-stat-number--accent">{sellerInfo.accountLifetime}</span>
                        <span className="profile-stat-label">Joined</span>
                    </div>

                    <div className="profile-stat">
                        <span className="profile-stat-number profile-stat-number--accent">{sellerInfo.location || "N/A"}</span>
                        <span className="profile-stat-label">Location</span>
                    </div>

                    <div className="profile-stat">
                        <span className="profile-stat-number profile-stat-number--accent">{sellerInfo.openingHours || "N/A"}</span>
                        <span className="profile-stat-label">Opening hours</span>
                    </div>
                </div>

                <div className="profile-section-row">
                    <section className="profile-section">
                        <h2 className="profile-section-title">Account details</h2>

                        <div className="profile-field">
                            <span className="profile-field-label">Seller name</span>
                            {editMode ? (
                                <input
                                    className="seller-profile-input"
                                    type="text"
                                    value={formValues.sellerName}
                                    onChange={handleChange("sellerName")}
                                />
                            ) : (
                                <span className="profile-field-value">{sellerInfo.sellerName || "N/A"}</span>
                            )}
                        </div>

                        <div className="profile-field">
                            <span className="profile-field-label">Account lifetime</span>
                            <span className="profile-field-value">{sellerInfo.accountLifetime || "N/A"}</span>
                        </div>

                        <div className="profile-field">
                            <span className="profile-field-label">Contact</span>
                            {editMode ? (
                                <input
                                    className="seller-profile-input"
                                    type="text"
                                    value={formValues.contactStub}
                                    onChange={handleChange("contactStub")}
                                />
                            ) : (
                                <span className="profile-field-value">{sellerInfo.contactStub || "N/A"}</span>
                            )}
                        </div>
                    </section>

                    <section className="profile-section">
                        <h2 className="profile-section-title">Business details</h2>

                        <div className="profile-field">
                            <span className="profile-field-label">Location</span>
                            {editMode ? (
                                <input
                                    className="seller-profile-input"
                                    type="text"
                                    value={formValues.location}
                                    onChange={handleChange("location")}
                                />
                            ) : (
                                <span className="profile-field-value">{sellerInfo.location || "N/A"}</span>
                            )}
                        </div>

                        <div className="profile-field">
                            <span className="profile-field-label">Opening hours</span>
                            {editMode ? (
                                <input
                                    className="seller-profile-input"
                                    type="text"
                                    value={formValues.openingHours}
                                    onChange={handleChange("openingHours")}
                                />
                            ) : (
                                <span className="profile-field-value">{sellerInfo.openingHours || "N/A"}</span>
                            )}
                        </div>
                    </section>
                </div>
            </div>
        </div>
    );
}

export default SellerProfilePage;