import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import NavBar from "../reusableComponents/navBar";
import "./profile.css";
import { getData } from "../reusableComponents/api.jsx";

const BADGE_IMAGE_PATHS = {
  "explorer": "/badges/explorer.png",
  "discoverer": "/badges/discoverer.png",
  "adventurer": "/badges/adventurer.png",
  "master": "/badges/master.png",
  "eco starter": "/badges/eco_starter.png",
  "eco friend": "/badges/eco_friend.png",
  "climate hero": "/badges/climate_hero.png",
  "planet saver": "/badges/planet_saver.png",
};

const BADGE_IMAGE_ALIASES = {
  "no waste hero": "eco starter",
  "early bird": "explorer",
};

function normalizeBadgeName(value) {
  return String(value || "")
    .trim()
    .toLowerCase()
    .replace(/_/g, " ")
    .replace(/\s+/g, " ");
}

function getBadgeImagePath(badgeName) {
  const normalized = normalizeBadgeName(badgeName);
  const resolvedName = BADGE_IMAGE_ALIASES[normalized] || normalized;
  return BADGE_IMAGE_PATHS[resolvedName] || "/badges/explorer.png";
}

function getReservationSortTime(reservation) {
  const raw = reservation?.timestamp || reservation?.created_at || reservation?.collected_at;
  const parsed = new Date(raw);
  return Number.isNaN(parsed.getTime()) ? 0 : parsed.getTime();
}

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
    return payload?.consumer_id ?? payload?.user_id ?? payload?.id ?? null;
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
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user_type")
    navigate("/login");
  }, [navigate]);

  // loads profile data, game summary, and reservations
  const load = useCallback(async () => {
    setError(null);

    try {
      let consumerId =
        getConsumerIdFromToken() ||
        localStorage.getItem("consumer_id") ||
        localStorage.getItem("consumerId");

      if (!consumerId) {
        const consumerList = await getData("marketplace/consumer/list", {}, true);
        if (Array.isArray(consumerList) && consumerList.length > 0) {
          consumerId = consumerList[0]?.consumer_id ?? consumerList[0]?.id ?? null;
        }
      }

      if (!consumerId) throw new Error("Could not determine buyer account. Please log in again.");

      localStorage.setItem("consumer_id", String(consumerId));

      const [userData, summaryData, reservationsData] = await Promise.all([
        getData(`marketplace/consumer/${consumerId}/`, {}, true),
        getData("game/summary/", {}, true),
        getData("marketplace/reservations/list", {}, true),
      ]);

      if (!userData || userData.detail) {
        throw new Error(
          typeof userData?.detail === "string"
            ? userData.detail
            : "Failed to load buyer profile"
        );
      }

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
        Array.isArray(reservationsData)
          ? [...reservationsData].sort(
              (a, b) => getReservationSortTime(b) - getReservationSortTime(a)
            )
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
      <div className="buyer-page profile-page">
        <NavBar />
        <div className="buyer-container profile-state">
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
      <div className="buyer-page profile-page">
        <NavBar />
        <div className="buyer-container profile-state">
          <p className="profile-loading">Loading…</p>
        </div>
      </div>
    );
  }

  const badges = Array.isArray(summary.badges) ? summary.badges : [];

  return (
    <div className="buyer-page profile-page">
      <NavBar />

      <section className="buyer-hero profile-banner">
        <div className="profile-banner-inner">
          <div className="profile-avatar">
            {user.display_name ? user.display_name[0].toUpperCase() : "?"}
          </div>

          <div className="profile-identity">
            <h1 className="profile-name">{user.display_name || "Unknown"}</h1>
          </div>

          <div className="profile-actions">
            <button className="profile-btn-ghost profile-btn-ghost--light" type="button" disabled>
              Edit profile
            </button>
            <button className="profile-btn-ghost profile-btn-ghost--light" type="button" onClick={handleLogout}>
              Log out
            </button>
          </div>
        </div>
      </section>

      <div className="buyer-container profile-wrap">
        <div className="profile-stats-row">
          <div className="profile-stat">
            <span className="profile-stat-number profile-stat-number--accent">{summary.total_rescued_bundles}</span>
            <span className="profile-stat-label">Bundles rescued</span>
          </div>

          <div className="profile-stat-divider" />

          <div className="profile-stat">
            <span className="profile-stat-number profile-stat-number--accent">{summary.current_streak_weeks}</span>
            <span className="profile-stat-label">Week streak</span>
          </div>

          <div className="profile-stat-divider" />

          <div className="profile-stat">
            <span className="profile-stat-number profile-stat-number--accent">{summary.unique_categories_rescued}</span>
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
              <div className="profile-badge-grid">
              {badges.map((badge) => (
                <div key={badge} className="profile-badge-tile">
                  <img
                    src={getBadgeImagePath(badge)}
                    alt={badge}
                    className="profile-badge-image"
                  />
                  <div className="profile-badge-name">{badge}</div>
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
                        <td>{formatDate(r.timestamp || r.created_at || r.collected_at)}</td>
                        <td>{r.claim_code || "N/A"}</td>
                        <td>{r.posting || r.posting_id || "N/A"}</td>
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
