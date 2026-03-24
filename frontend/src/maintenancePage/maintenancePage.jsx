import React, { useState } from "react";
import "./maintenance.css";

const api = import.meta.env.VITE_API_HOST;
const port = import.meta.env.VITE_API_PORT;

const base = `http://${api}:${port}`;

const API_BASE_URL = base;

export default function MaintenancePage() {
  const [query, setQuery] = useState("SELECT * FROM bundle_posting;");
  const [results, setResults] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const runQuery = async () => {
    const token = localStorage.getItem("access_token")

    if (!token) {
      setError("No access token found. Please log in as a maintainer.");
      setResults([]);
      return;
    }

    const url = `${API_BASE_URL}/maintainer/sql`;

    console.log("Running SQL query at:", url);

    try {
      setLoading(true);
      setError("");
      setResults([]);

      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        const text = await response.text();
        console.error("Backend error:", text);
        throw new Error(`Request failed (${response.status})`);
      }

      const text = await response.text();

      let parsed;
      try {
        parsed = JSON.parse(text);
      } catch {
        parsed = text;
      }

      setResults(parsed);
    } catch (err) {
      console.error("SQL request failed:", err);
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

          {results && results.length > 0 && (
            <pre className="maintenance-results">
              {JSON.stringify(results, null, 2)}
            </pre>
          )}
        </section>
      </div>
    </main>
  );
}