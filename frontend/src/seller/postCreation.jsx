/* --- File Description --- */
/* Blah Blah Blah I got bored of this shit ICL */

/* --- Import Statements --- */
import { useState } from "react";
import NavBar from "../reusableComponents/navBar";
import { useGetData, postData } from "../reusableComponents/api";
import "./postCreation.css";

/* --- Helper to get day of week (1-7, Monday-Sunday) --- */
function getCurrentDayOfWeek() {
    const day = new Date().getDay();
    return day === 0 ? 7 : day;
}

/* --- Main Page Function --- */
function PostCreation() {
    const [selectedAllergenIds, setSelectedAllergenIds] = useState([]);
    const [timeWindow, setTimeWindow] = useState("09:00-10:00");
    const [category, setCategory] = useState("bakery");
    const [quantity, setQuantity] = useState(1);
    const [price, setPrice] = useState("");
    const [contents, setContents] = useState("");
    const [status, setStatus] = useState("active");
    const [submitStatus, setSubmitStatus] = useState("");
    const [forecastData, setForecastData] = useState(null);
    const [forecastLoading, setForecastLoading] = useState(false);
    const [showForecastModal, setShowForecastModal] = useState(false);

    const { data: allergens, loading: allergensLoading } = useGetData("marketplace/allergens/", {}, false);

    function toggleAllergen(allergenId) {
        setSelectedAllergenIds(prev =>
            prev.includes(allergenId)
                ? prev.filter(id => id !== allergenId)
                : [...prev, allergenId]
        );
    }

    async function handleLoadForecast() {
        try {
            setForecastLoading(true);
            const qty = parseInt(quantity) || 1;
            const priceValue = price ? parseFloat(price) : null;
            
            const forecastResult = await postData("forecast/prediction/", {
                category: category,
                day_of_week: getCurrentDayOfWeek(),
                time_window: timeWindow,
                no_bundles: qty,
                price: priceValue,
            }, true);
            
            if (forecastResult && forecastResult.primary_forecast) {
                setForecastData(forecastResult);
                setShowForecastModal(true);
            } else {
                alert("Failed to load forecast: " + (forecastResult?.error || "Unknown error"));
            }
        } catch (err) {
            console.error("Error loading forecast:", err);
            alert("Error loading forecast");
        } finally {
            setForecastLoading(false);
        }
    }

    function closeForecastModal() {
        setShowForecastModal(false);
    }

    async function handlePostListing() {
        try {
            setSubmitStatus("Posting...");
            const qty = parseInt(quantity) || 1;
            const result = await postData("marketplace/bundle/create", {
                category: category,
                contents: contents || "Bundle",
                quantity: qty,
                quantity_remaining: qty,
                price: parseFloat(price) || 0,
                pickup_window: timeWindow,
                status: status,
            }, true);
            
            console.log("Post listing result:", result);
            
            if (result && result.posting_id) {
                setSubmitStatus("Posted successfully!");
                setTimeWindow("09:00-10:00");
                setCategory("bakery");
                setQuantity(1);
                setPrice("");
                setContents("");
                setSelectedAllergenIds([]);
                setTimeout(() => setSubmitStatus(""), 3000);
            } else {
                setSubmitStatus("Failed to post listing");
            }
        } catch (err) {
            console.error("Error posting listing:", err);
            setSubmitStatus("Error posting listing");
        }
    }

    return (
        <div className="buyer-page">
            <NavBar user_type={"seller"} />
            <section className="buyer-hero">
                <p className="buyer-hero-label">Create</p>
                <h1 className="buyer-hero-title">New Bundle Listing</h1>
                <p className="buyer-hero-subtitle">Add a new bundle to the marketplace with details and allergen information.</p>
            </section>
            <div className="buyer-container">
                <div className="bundleForecast-panel">
                <p>Time Window</p>
                <select value={timeWindow} onChange={(e) => setTimeWindow(e.target.value)}>
                    <option value="00:00-01:00">0-1am</option>
                    <option value="01:00-02:00">1-2am</option>
                    <option value="02:00-03:00">2-3am</option>
                    <option value="03:00-04:00">3-4am</option>
                    <option value="04:00-05:00">4-5am</option>
                    <option value="05:00-06:00">5-6am</option>
                    <option value="06:00-07:00">6-7am</option>
                    <option value="07:00-08:00">7-8am</option>
                    <option value="08:00-09:00">8-9am</option>
                    <option value="09:00-10:00">9-10am</option>
                    <option value="10:00-11:00">10-11am</option>
                    <option value="11:00-12:00">11-12pm</option>
                    <option value="12:00-13:00">12-1pm</option>
                    <option value="13:00-14:00">1-2pm</option>
                    <option value="14:00-15:00">2-3pm</option>
                    <option value="15:00-16:00">3-4pm</option>
                    <option value="16:00-17:00">4-5pm</option>
                    <option value="17:00-18:00">5-6pm</option>
                    <option value="18:00-19:00">6-7pm</option>
                    <option value="19:00-20:00">7-8pm</option>
                    <option value="20:00-21:00">8-9pm</option>
                    <option value="21:00-22:00">9-10pm</option>
                    <option value="22:00-23:00">10-11pm</option>
                    <option value="23:00-00:00">11-12am</option>
                </select>
                <hr />
                <p>Category</p>
                <select value={category} onChange={(e) => setCategory(e.target.value)}>
                    <option value="bakery">Bakery</option>
                    <option value="hot_meals">Hot Meals</option>
                    <option value="fresh_produce">Fresh Produce</option>
                    <option value="dairy">Dairy</option>
                    <option value="prepared_salads">Prepared Salads</option>
                    <option value="desserts">Desserts</option>
                </select>
                <hr />
                <p>Bundle Description</p>
                <input 
                    type="text" 
                    value={contents} 
                    onChange={(e) => setContents(e.target.value)}
                    placeholder="e.g., Fresh vegetables, misc. pastries"
                />
                <hr />
                <p>Number of Bundles to Create</p>
                <input 
                    type="number" 
                    min="1" 
                    value={quantity}
                    onChange={(e) => setQuantity(e.target.value)}
                />
                <hr />
                <p>Price per Bundle (£)</p>
                <input 
                    type="number" 
                    step="0.01" 
                    min="0"
                    value={price}
                    onChange={(e) => setPrice(e.target.value)}
                    placeholder="0.00"
                />
                <hr />
                <p>Status</p>
                <select value={status} onChange={(e) => setStatus(e.target.value)}>
                    <option value="active">Active</option>
                    <option value="expired">Expired</option>
                    <option value="completed">Completed</option>
                    <option value="cancelled">Cancelled</option>
                </select>
                <hr />
                <p>Allergens</p>
                {allergensLoading ? (
                    <p>Loading allergens...</p>
                ) : (
                    <div className="allergen-checkboxes">
                        {allergens && allergens.map(allergen => (
                            <label key={allergen.allergen_id} className="allergen-checkbox-label">
                                <input
                                    type="checkbox"
                                    checked={selectedAllergenIds.includes(allergen.allergen_id)}
                                    onChange={() => toggleAllergen(allergen.allergen_id)}
                                />
                                {allergen.name}
                            </label>
                        ))}
                    </div>
                )}
                <hr />
                <p>Post Bundle Listing</p>
                <button className="btn-primary" onClick={handlePostListing}>Post Listing</button>
                <button 
                    className="btn-secondary" 
                    onClick={handleLoadForecast}
                    disabled={forecastLoading}
                    style={{marginLeft: "10px"}}
                >
                    {forecastLoading ? "Loading..." : "Load Forecast"}
                </button>
                {submitStatus && <p className="submit-status">{submitStatus}</p>}
            </div>
            </div>

            {/* Forecast Modal */}
            {showForecastModal && forecastData && (
                <div className="forecast-modal-overlay" onClick={closeForecastModal}>
                    <div className="forecast-modal" onClick={(e) => e.stopPropagation()}>
                        <button className="forecast-modal-close" onClick={closeForecastModal}>×</button>
                        <h2>Demand Forecast</h2>
                        
                        <div className="forecast-section">
                            <h3>Primary Forecast</h3>
                            <p><strong>Predicted Reservations:</strong> {forecastData.primary_forecast.predicted_reservations}</p>
                            <p><strong>No-show Probability:</strong> {(forecastData.primary_forecast.no_show_probability * 100).toFixed(2)}%</p>
                        </div>

                        <div className="forecast-section">
                            <h3>Model Predictions</h3>
                            <div className="models-grid">
                                {Object.entries(forecastData.model_predictions).map(([modelName, modelData]) => (
                                    <div key={modelName} className="model-card">
                                        <h4>{modelName.replace(/_/g, ' ')}</h4>
                                        <p><strong>Predicted Reservations:</strong> {modelData.predicted_reservations}</p>
                                        <p><strong>No-show Probability:</strong> {(modelData.no_show_probability * 100).toFixed(2)}%</p>
                                        <p className="model-desc">{modelData.description}</p>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {forecastData.recommended_price && (
                            <div className="forecast-section">
                                <h3>Recommended Price</h3>
                                <p className="recommendation-price">£{forecastData.recommended_price.toFixed(2)}</p>
                            </div>
                        )}

                        <div className="forecast-section">
                            <h3>Recommendation</h3>
                            <p><strong>Action:</strong> {forecastData.recommendation.action}</p>
                            <p><strong>Confidence:</strong> {forecastData.recommendation.confidence}</p>
                            <p><strong>Rationale:</strong> {forecastData.recommendation.rationale}</p>
                        </div>

                        <button className="btn-primary" onClick={closeForecastModal}>Close</button>
                    </div>
                </div>
            )}
        </div>
    );
}

/* --- Export --- */
export default PostCreation;
