import React, { useEffect, useState } from "react";
import NavBar from "../reusableComponents/navBar";
import { createIssue, fetchMyIssues } from "../api-legacy/issueReporting";
import "./issueReportingPage.css";

const CATEGORY_OPTIONS = [
  "Order issue",
  "Delivery issue",
  "Payment issue",
  "Account issue",
  "Other",
];

export default function IssueReportingPage() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [category, setCategory] = useState(CATEGORY_OPTIONS[0]);
  const [orderId, setOrderId] = useState("");

  const [issues, setIssues] = useState([]);
  const [isLoadingIssues, setIsLoadingIssues] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const loadIssues = async () => {
    setIsLoadingIssues(true);
    try {
      const data = await fetchMyIssues();
      setIssues(Array.isArray(data) ? data : []);
    } catch {
      setIssues([]);
    } finally {
      setIsLoadingIssues(false);
    }
  };

  useEffect(() => {
    loadIssues();
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setSuccess("");
    setIsLoading(true);

    try {
      await createIssue({
        title: title.trim(),
        description: description.trim(),
        category,
        orderId: orderId.trim(),
      });

      setSuccess("Issue submitted successfully.");
      setTitle("");
      setDescription("");
      setCategory(CATEGORY_OPTIONS[0]);
      setOrderId("");
      await loadIssues();
    } catch (err) {
      const message =
        typeof err?.message === "string" && err.message.trim()
          ? err.message
          : "Could not submit issue. Please try again.";
      setError(message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="issue-dashboard-page">
      <NavBar />
      <div className="issue-dashboard-container">
        <section className="issue-list-panel">
          <h1 className="issue-dashboard-title">Issue Dashboard</h1>
          <p className="issue-dashboard-subtitle">Your submitted reports</p>

          {isLoadingIssues ? (
            <p className="issue-empty-state">Loading issues...</p>
          ) : issues.length === 0 ? (
            <p className="issue-empty-state">No issues reported yet.</p>
          ) : (
            <div className="issue-list">
              {issues.map((issue, index) => {
                const key = issue.id || issue.issue_id || index;
                const displayTitle = issue.title || "Untitled issue";
                const displayCategory = issue.category || "Uncategorised";
                const displayStatus = issue.status || "Open";
                const displayDescription =
                  issue.description || "No description provided.";

                return (
                  <article key={key} className="issue-card">
                    <div className="issue-card-header">
                      <h3>{displayTitle}</h3>
                      <span className="issue-status-pill">{displayStatus}</span>
                    </div>
                    <p className="issue-card-category">{displayCategory}</p>
                    <p className="issue-card-description">{displayDescription}</p>
                  </article>
                );
              })}
            </div>
          )}
        </section>

        <aside className="issue-form-panel">
          <h2 className="issue-form-title">New Report</h2>

          {error && <div className="issue-feedback issue-error">{error}</div>}
          {success && <div className="issue-feedback issue-success">{success}</div>}

          <form className="issue-form" onSubmit={handleSubmit}>
            <label className="issue-label">
              Title
              <input
                className="issue-input"
                value={title}
                onChange={(event) => setTitle(event.target.value)}
                placeholder="Short summary of the issue"
                required
              />
            </label>

            <label className="issue-label">
              Category
              <select
                className="issue-input"
                value={category}
                onChange={(event) => setCategory(event.target.value)}
              >
                {CATEGORY_OPTIONS.map((option) => (
                  <option key={option} value={option}>
                    {option}
                  </option>
                ))}
              </select>
            </label>

            <label className="issue-label">
              Order ID (optional)
              <input
                className="issue-input"
                value={orderId}
                onChange={(event) => setOrderId(event.target.value)}
                placeholder="Related order id"
              />
            </label>

            <label className="issue-label">
              Description
              <textarea
                className="issue-input issue-textarea"
                value={description}
                onChange={(event) => setDescription(event.target.value)}
                placeholder="Describe the issue in detail"
                rows={6}
                required
              />
            </label>

            <button className="issue-submit-btn" disabled={isLoading}>
              {isLoading ? "Submitting..." : "Submit issue"}
            </button>
          </form>
        </aside>
        </div>
      </div>
  );
}
