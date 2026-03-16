import React, { useState } from "react";
import "./MaintenancePage.css";

export default function MaintenancePage() {
  const [query, setQuery] = useState("SELECT * FROM maintainer_maintainer;");
  const [results, setResults] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const runQuery = async () => {
    const token =
      localStorage.getItem("accessToken") ||
      localStorage.getItem("access") ||
      localStorage.getItem("token");

    if (!token) {
      setError("No access token found. Please log in as a maintainer.");
      setResults([]);
      return;
    }

    try {
      setLoading(true);
      setError("");
      setResults([]);

      const response = await fetch(
        `${import.meta.env.VITE_API_BASE_URL}/maintainer/maintainer/sql`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ query }),
        }
      );

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }

      const text = await response.text();
      const parsed = JSON.parse(text);

      setResults(parsed);
    } catch (err) {
      setError(err.message || "Something went wrong while running the query.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="maintenance-page">
      <div className="maintenance-container">
        <h1>Developer Maintenance Page</h1>
        <p className="maintenance-description">
          This page allows authorised maintainers to run SQL queries on the
          Project-Ate database for maintenance and inspection tasks.
        </p>

        <section className="maintenance-section">
          <h2>SQL Query</h2>
          <textarea
            className="maintenance-textarea"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            rows={10}
            placeholder="Enter an SQL query..."
          />
          <button
            className="maintenance-button"
            onClick={runQuery}
            disabled={loading}
          >
            {loading ? "Running..." : "Run Query"}
          </button>
        </section>

        <section className="maintenance-section">
          <h2>Query Results</h2>

          {error && <div className="maintenance-error">{error}</div>}

          {!error && results.length === 0 && !loading && (
            <div className="maintenance-empty">
              No results to display yet.
            </div>
          )}

          {results.length > 0 && (
            <pre className="maintenance-results">
              {JSON.stringify(results, null, 2)}
            </pre>
          )}
        </section>
      </div>
    </main>
  );
}