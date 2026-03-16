import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { fetchConsumerProfile, fetchConsumerReservations } from "../api-legacy/marketplace";
import { fetchGameSummary } from "../api-legacy/game";
import NavBar from "../reusableComponents/navBar";
import "./BuyerProfilePage.css";

// toggle to false when auth is complete and endpoints are ready
const USE_MOCK_DATA = true;

// mock consumer profile - matches GET /marketplace/consumer/<id>/ response shape
const MOCK_USER = {
  consumer_id: 1,
  display_name: "Will Brown",
  streak: 5,
};

// mock game summary - matches GET /game/api/game/summary/ response shape
const MOCK_SUMMARY = {
  total_rescued_bundles: 12,
  estimated_co2e_saved_kg: 28.5,
  current_streak_weeks: 3,
  badges: ["First Rescue", "Eco Warrior"],
};

// mock reservations - matches GET /buyer/getreservations/<id>/ response shape
const MOCK_RESERVATIONS = [
  {
    reservation_id: 1,
    posting_id: 101,
    claim_code: "ABC123",
    status: "collected",
    created_at: "2026-03-08T17:31:00Z",
  },
  {
    reservation_id: 2,
    posting_id: 102,
    claim_code: "DEF456",
    status: "collected",
    created_at: "2026-03-05T12:10:00Z",
  },
  {
    reservation_id: 3,
    posting_id: 103,
    claim_code: "GHI789",
    status: "reserved",
    created_at: "2026-02-28T18:45:00Z",
  },
  {
    reservation_id: 4,
    posting_id: 104,
    claim_code: "JKL012",
    status: "no-show",
    created_at: "2026-02-20T09:15:00Z",
  },
];

// formats api timestamps into readable dates
function formatDate(isoString) {
  if (!isoString) return "—";
  return new Date(isoString).toLocaleDateString(undefined, {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

export default function BuyerProfilePage() {
  const navigate = useNavigate();

  // consumer profile from api
  const [user, setUser] = useState(null);

  // game stats and badges
  const [summary, setSummary] = useState(null);

  // reservation history
  const [reservations, setReservations] = useState([]);

  // error state for failed api requests
  const [error, setError] = useState(null);

  // clears JWT tokens and returns to login
  const handleLogout = useCallback(() => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    navigate("/login");
  }, [navigate]);

  // loads profile data, game summary, and reservations
  const load = useCallback(async () => {
    setError(null);

    try {
      if (USE_MOCK_DATA) {
        setUser(MOCK_USER);
        setSummary(MOCK_SUMMARY);
        setReservations(MOCK_RESERVATIONS);
        return;
      }

      // TODO: get consumerId from auth context once auth is complete
      const consumerId = null; // placeholder — replace with real id from auth
      if (!consumerId) throw new Error("Not authenticated");

      const [userData, summaryData, reservationsData] = await Promise.all([
        fetchConsumerProfile(consumerId),
        fetchGameSummary(),
        fetchConsumerReservations(consumerId),
      ]);

      setUser(userData);
      setSummary(summaryData);
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
              <span> {user.streak ?? 0} week{user.streak !== 1 ? "s" : ""} streak — keep it up!</span>
              {USE_MOCK_DATA && <span className="profile-mock-tag">Mock data</span>}
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
            <span className="profile-stat-number" style={{color: "var(--green)"}}>{badges.length}</span>
            <span className="profile-stat-label">Badges earned</span>
          </div>
        </div>

        <div className="profile-section-row">
          <section className="profile-section">
            <h2 className="profile-section-title">Account details</h2>

            <div className="profile-field">
              <span className="profile-field-label">Display name</span>
              <span className="profile-field-value">{user.display_name || "—"}</span>
            </div>

            <div className="profile-field">
              <span className="profile-field-label">Streak</span>
              <span className="profile-field-value">{user.streak ?? 0} weeks</span>
            </div>

            <div className="profile-field">
              <span className="profile-field-label">CO₂e saved</span>
              <span className="profile-field-value">
                {summary.estimated_co2e_saved_kg != null
                  ? `${summary.estimated_co2e_saved_kg} kg`
                  : "—"}
              </span>
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
                No badges yet — keep rescuing bundles to earn them.
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
                        <td>{r.claim_code || "—"}</td>
                        <td>{r.posting_id || "—"}</td>
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
