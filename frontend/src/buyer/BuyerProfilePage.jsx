import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import NavBar from "../reusableComponents/navBar";
import "./BuyerProfilePage.css";
import { getData } from "../reusableComponents/api.jsx";

// formats api timestamps into readable dates
function formatDate(isoString) {
  if (!isoString) return "N/A";
  return new Date(isoString).toLocaleDateString(undefined, {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

function getConsumerIdFromToken() {
  const token = localStorage.getItem("access_token");
  if (!token) return null;

  try {
    const payload = jwtDecode(token);
    return payload?.user_id ?? payload?.id ?? null;
  } catch {
    return null;
  }
}

export default function BuyerProfilePage() {
  const navigate = useNavigate();

  // consumer profile from api
  const [user, setUser] = useState(null);

  // game summary from api
  const [summary, setSummary] = useState(null);

  // reservation history
  const [reservations, setReservations] = useState([]);

  // error state for failed api requests
  const [error, setError] = useState(null);

  // clears JWT tokens and returns to login
  const handleLogout = useCallback(() => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh");
    navigate("/login");
  }, [navigate]);

  // loads profile data, game summary, and reservations
  const load = useCallback(async () => {
    setError(null);

    try {
      const consumerId = getConsumerIdFromToken();
      if (!consumerId) throw new Error("Not authenticated");

      const [userData, summaryData, reservationsData] = await Promise.all([
        getData(`marketplace/consumer/${consumerId}/`, {}, true),
        getData("game/summary/", {}, true),
        getData(`marketplace/reservations/${consumerId}/`, {}, true),
      ]);

      setUser(userData);
      setSummary({
        current_streak_weeks: summaryData?.current_streak_weeks ?? 0,
        has_rescued_this_week: !!summaryData?.has_rescued_this_week,
        total_rescued_bundles: summaryData?.total_rescued_bundles ?? 0,
        estimated_co2e_saved_kg: summaryData?.estimated_co2e_saved_kg ?? null,
        badges: Array.isArray(summaryData?.badges) ? summaryData.badges : [],
        unique_categories_rescued: summaryData?.unique_categories_rescued ?? 0,
      });
      setReservations(
        Array.isArray(reservationsData?.reservations)
          ? reservationsData.reservations
          : []
      );
    } catch (e) {
      const message =
        e && typeof e === "object" && "message" in e
          ? e.message
          : "Failed to load profile";

      setError(new Error(message));
    }
  }, []);

  // load profile when page mounts
  useEffect(() => {
    load();
  }, [load]);

  // error state ui
  if (error) {
    return (
      <div className="profile-page">
        <NavBar />
        <div className="profile-state">
          <div className="profile-error">
            <h2>Profile</h2>
            <p>{error.message}</p>
            <button className="profile-btn-ghost" type="button" onClick={load}>
              Try again
            </button>
          </div>
        </div>
      </div>
    );
  }

  // loading state while api requests run
  if (!user || !summary) {
    return (
      <div className="profile-page">
        <NavBar />
        <div className="profile-state">
          <p className="profile-loading">Loading…</p>
        </div>
      </div>
    );
  }

  const badges = Array.isArray(summary.badges) ? summary.badges : [];

  return (
    <div className="profile-page">
      <NavBar />

      <div className="profile-banner" style={{background: "linear-gradient(135deg, #1B2D23, #2D6A4F)"}}>
        <div className="profile-banner-inner">
          <div className="profile-avatar" style={{background: "var(--green-light)", color: "white", border: "3px solid rgba(255,255,255,0.3)"}}>
            {user.display_name ? user.display_name[0].toUpperCase() : "?"}
          </div>

          <div className="profile-identity">
            <h1 className="profile-name" style={{color: "white"}}>{user.display_name || "Unknown"}</h1>
            <p className="profile-meta" style={{color: "var(--green-pale)"}}>              
              <span>
                {summary.current_streak_weeks ?? 0} week{summary.current_streak_weeks !== 1 ? "s" : ""} streak
                {summary.has_rescued_this_week ? " • rescued this week" : " • no rescue this week yet"}
              </span>
            </p>
          </div>

          <div className="profile-actions">
            <button className="profile-btn-ghost" type="button" disabled style={{color: "white", borderColor: "rgba(255,255,255,0.3)"}}>
              Edit profile
            </button>
            <button className="profile-btn-ghost" type="button" onClick={handleLogout} style={{color: "white", borderColor: "rgba(255,255,255,0.3)"}}>
              Log out
            </button>
          </div>
        </div>
      </div>

      <div className="profile-wrap">
        <div className="profile-stats-row">
          <div className="profile-stat">
            <span className="profile-stat-number" style={{color: "var(--green)"}}>{summary.total_rescued_bundles}</span>
            <span className="profile-stat-label">Bundles rescued</span>
          </div>

          <div className="profile-stat-divider" />

          <div className="profile-stat">
            <span className="profile-stat-number" style={{color: "var(--green)"}}>{summary.current_streak_weeks}</span>
            <span className="profile-stat-label">Week streak</span>
          </div>

          <div className="profile-stat-divider" />

          <div className="profile-stat">
            <span className="profile-stat-number" style={{color: "var(--green)"}}>{summary.unique_categories_rescued}</span>
            <span className="profile-stat-label">Categories rescued</span>
          </div>
        </div>

        <div className="profile-section-row">
          <section className="profile-section">
            <h2 className="profile-section-title">Account details</h2>

            <div className="profile-field">
              <span className="profile-field-label">Display name</span>
              <span className="profile-field-value">{user.display_name || "N/A"}</span>
            </div>

            <div className="profile-field">
              <span className="profile-field-label">Streak</span>
              <span className="profile-field-value">{summary.current_streak_weeks ?? 0} weeks</span>
            </div>

            <div className="profile-field">
              <span className="profile-field-label">CO₂e saved</span>
              <span className="profile-field-value">
                {summary.estimated_co2e_saved_kg != null
                  ? `${summary.estimated_co2e_saved_kg} kg`
                  : "N/A"}
              </span>
            </div>

            <div className="profile-field">
              <span className="profile-field-label">Rescued this week</span>
              <span className="profile-field-value">{summary.has_rescued_this_week ? "Yes" : "No"}</span>
            </div>

            <div className="profile-field">
              <span className="profile-field-label">Unique categories rescued</span>
              <span className="profile-field-value">{summary.unique_categories_rescued}</span>
            </div>
          </section>

          <section className="profile-section">
            <h2 className="profile-section-title">Badges</h2>

            {badges.length > 0 ? (
              <div style={{display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "1rem"}}>
              {badges.map((badge) => (
                <div key={badge} style={{
                  background: "var(--green-pale)",
                  borderRadius: "16px",
                  padding: "1.2rem 1rem",
                  textAlign: "center",
                  border: "1px solid var(--green-light)",
                  transition: "transform 0.2s"
                }}>
                  <div style={{fontSize: "1.8rem", marginBottom: "0.5rem"}}>🏅</div>
                  <div style={{fontWeight: "700", color: "var(--green)", fontSize: "0.85rem"}}>{badge}</div>
                </div>
              ))}
            </div>
            ) : (
              <p className="profile-empty">
                No badges yet. Keep rescuing bundles to earn them.
              </p>
            )}
          </section>

          <section className="profile-section profile-section--full">
            <h2 className="profile-section-title">Full Rescue History</h2>

            {reservations.length > 0 ? (
              <div className="profile-table-wrap">
                <table className="profile-table">
                  <thead>
                    <tr>
                      <th>Date</th>
                      <th>Claim code</th>
                      <th>Bundle ID</th>
                      <th>Status</th>
                    </tr>
                  </thead>

                  <tbody>
                    {reservations.map((r) => (
                      <tr key={r.reservation_id}>
                        <td>{formatDate(r.created_at)}</td>
                        <td>{r.claim_code || "N/A"}</td>
                        <td>{r.posting_id || "N/A"}</td>
                        <td>
                          {r.status && (
                            <span className="profile-status-badge">{r.status}</span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="profile-empty">No reservations yet.</p>
            )}
          </section>
        </div>
      </div>
    </div>
  );
}
