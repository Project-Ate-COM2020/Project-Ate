/* --- File Description --- */

/* The seller issues page, made by Lucas */

/* --- Current Problems and TODOS --- */

// Not much I don't think

/* --- Import Statements --- */
import React, { useEffect, useState } from "react";
import NavBar from "../reusableComponents/navBar";
import { getData, postData } from "../reusableComponents/api";
import "./issuesPage.css";

// defining constant
const STATUS_OPTIONS = ["open", "responded", "resolved"];
const FILTER_OPTIONS = ["all", ...STATUS_OPTIONS];


/* --- Main Page Function --- */
export default function SellerIssuesPage() {
  const [issues, setIssues] = useState([]);
  const [isLoadingIssues, setIsLoadingIssues] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  
  const [selectedIssueId, setSelectedIssueId] = useState(null);
  const [responseText, setResponseText] = useState("");
  const [statusValue, setStatusValue] = useState("open");
  const [isUpdating, setIsUpdating] = useState(false);
  const [activeFilter, setActiveFilter] = useState("all");

  const loadIssues = async () => {
    setIsLoadingIssues(true);
    try {
      const data = await getData("issues/seller/");
      setIssues(Array.isArray(data) ? data : []);
    } catch (err) {
      setIssues([]);
      setError("Failed to load issues");
    } finally {
      setIsLoadingIssues(false);
    }
  };

  useEffect(() => {
    loadIssues();
  }, []);

  const handleSelectIssue = (issue) => {
    setSelectedIssueId(issue.issue_id);
    setResponseText(issue.seller_response || "");
    setStatusValue(issue.status || "open");
    setError("");
    setSuccess("");
  };

  const handleClearSelection = () => {
    setSelectedIssueId(null);
    setResponseText("");
    setStatusValue("open");
  };

  const handleSubmitResponse = async (event) => {
    event.preventDefault();
    setError("");
    setSuccess("");
    setIsUpdating(true);

    try {
      const response = await postData(
        `issues/seller/${selectedIssueId}/respond/`,
        {
          status: statusValue,
          seller_response: responseText.trim(),
        }
      );

      if (response?.error) {
        setError(response.error);
      } else {
        setSuccess("Issue updated successfully.");
        await loadIssues();
        handleClearSelection();
      }
    } catch (err) {
      const message =
        typeof err?.message === "string" && err.message.trim()
          ? err.message
          : "Could not update issue. Please try again.";
      setError(message);
    } finally {
      setIsUpdating(false);
    }
  };

  const currentIssue = issues.find((issue) => issue.issue_id === selectedIssueId);
  const filteredIssues = activeFilter === "all"
    ? issues
    : issues.filter((issue) => (issue.status || "open") === activeFilter);

  return (
    <div className="buyer-page seller-issues-page">
      <NavBar user_type={"seller"}/>
      <section className="buyer-hero">
        <p className="buyer-hero-label">Support</p>
        <h1 className="buyer-hero-title">Customer Queries</h1>
        <p className="buyer-hero-subtitle">Manage and respond to customer inquiries and issues.</p>
      </section>
      <div className="buyer-container">
        <div className="seller-issues-container">
        <section className="seller-issues-list-panel">
          <h1 className="seller-issues-title">Customer Queries</h1>
          <p className="seller-issues-subtitle">Open queries from customers</p>

          <div className="seller-issues-filter-row">
            <span className="seller-issues-filter-label">Filter:</span>
            <div className="seller-issues-filter-buttons">
              {FILTER_OPTIONS.map((option) => {
                const isActive = activeFilter === option;
                const label = option === "all"
                  ? "All"
                  : option.charAt(0).toUpperCase() + option.slice(1);

                return (
                  <button
                    key={option}
                    type="button"
                    className={`seller-issues-filter-btn ${isActive ? "active" : ""}`}
                    onClick={() => setActiveFilter(option)}
                  >
                    {label}
                  </button>
                );
              })}
            </div>
          </div>

          {isLoadingIssues ? (
            <p className="seller-issues-empty-state">Loading issues...</p>
          ) : filteredIssues.length === 0 ? (
            <p className="seller-issues-empty-state">No issues found for this stage.</p>
          ) : (
            <div className="seller-issues-list">
              {filteredIssues.map((issue, index) => {
                const key = issue.issue_id || index;
                const displayConsumer = issue.consumer?.display_name || "Unknown customer";
                const displayStatus = issue.status || "open";
                const displayType = (issue.type || "General inquiry")
                  .split("_")
                  .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                  .join(" ");
                const displayCategory = issue.posting?.category || "Unknown";
                const isSelected = selectedIssueId === issue.issue_id;

                return (
                  <article
                    key={key}
                    className={`seller-issue-card ${isSelected ? "selected" : ""}`}
                  >
                    <div className="seller-issue-card-header">
                      <div className="seller-issue-card-title-section">
                        <h3>{displayType}</h3>
                        <p className="seller-issue-card-customer">
                          {displayConsumer}
                        </p>
                      </div>
                      <span className={`seller-issue-status-pill status-${displayStatus}`}>
                        {displayStatus}
                      </span>
                    </div>
                    <p className="seller-issue-card-category">
                      Category: {displayCategory}
                    </p>
                    <p className="seller-issue-card-description">
                      {issue.description || "No description provided."}
                    </p>
                    {issue.seller_response && (
                      <p className="seller-issue-card-your-response">
                        Your response: {issue.seller_response}
                      </p>
                    )}
                    <button
                      className="seller-issue-reply-btn"
                      onClick={() => handleSelectIssue(issue)}
                    >
                      Reply
                    </button>
                  </article>
                );
              })}
            </div>
          )}
        </section>

        <aside className="seller-issues-response-panel">
          {selectedIssueId && currentIssue ? (
            <>
              <div className="seller-issues-response-header">
                <h2 className="seller-issues-response-title">Respond to Query</h2>
                <button
                  className="seller-issues-close-btn"
                  onClick={handleClearSelection}
                >
                  ✕
                </button>
              </div>

              <div className="seller-issue-details">
                <div className="seller-issue-detail-row">
                  <span className="seller-issue-detail-label">From:</span>
                  <span className="seller-issue-detail-value">
                    {currentIssue.consumer?.display_name || "Unknown"}
                  </span>
                </div>
                <div className="seller-issue-detail-row">
                  <span className="seller-issue-detail-label">Category:</span>
                  <span className="seller-issue-detail-value">
                    {currentIssue.type || "General"}
                  </span>
                </div>
                <div className="seller-issue-detail-row">
                  <span className="seller-issue-detail-label">Posting:</span>
                  <span className="seller-issue-detail-value">
                    {currentIssue.posting?.category || "Unknown"}
                  </span>
                </div>
                <div className="seller-issue-detail-row">
                  <span className="seller-issue-detail-label">Issue ID:</span>
                  <span className="seller-issue-detail-value">
                    #{currentIssue.issue_id}
                  </span>
                </div>
              </div>

              <div className="seller-issue-message">
                <p className="seller-issue-message-label">Customer's Message:</p>
                <div className="seller-issue-message-content">
                  {currentIssue.description || "No message provided."}
                </div>
              </div>

              {error && (
                <div className="seller-issue-feedback seller-issue-error">
                  {error}
                </div>
              )}
              {success && (
                <div className="seller-issue-feedback seller-issue-success">
                  {success}
                </div>
              )}

              <form
                className="seller-issue-response-form"
                onSubmit={handleSubmitResponse}
              >
                <label className="seller-issue-label">
                  Status
                  <select
                    className="seller-issue-input"
                    value={statusValue}
                    onChange={(event) => setStatusValue(event.target.value)}
                  >
                    {STATUS_OPTIONS.map((option) => (
                      <option key={option} value={option}>
                        {option.charAt(0).toUpperCase() + option.slice(1)}
                      </option>
                    ))}
                  </select>
                </label>

                <label className="seller-issue-label">
                  Your Response
                  <textarea
                    className="seller-issue-input seller-issue-textarea"
                    value={responseText}
                    onChange={(event) => setResponseText(event.target.value)}
                    placeholder="Type your response to the customer..."
                    rows={6}
                  />
                </label>

                <button
                  className="seller-issue-submit-btn"
                  disabled={isUpdating || !responseText.trim()}
                >
                  {isUpdating ? "Updating..." : "Send Response"}
                </button>
              </form>
            </>
          ) : (
            <div className="seller-issues-stats">
              <h2 className="seller-issues-stats-title">Overview</h2>
              <div className="seller-issues-stat-row">
                <div className="seller-issues-stat-card">
                  <div className="seller-issues-stat-number">{issues.length}</div>
                  <div className="seller-issues-stat-label">Total Issues</div>
                </div>
              </div>
              <div className="seller-issues-stat-row">
                <div className="seller-issues-stat-card stat-card-open">
                  <div className="seller-issues-stat-number">
                    {issues.filter((i) => i.status === "open").length}
                  </div>
                  <div className="seller-issues-stat-label">Open</div>
                </div>
                <div className="seller-issues-stat-card stat-card-responded">
                  <div className="seller-issues-stat-number">
                    {issues.filter((i) => i.status === "responded").length}
                  </div>
                  <div className="seller-issues-stat-label">Responded</div>
                </div>
              </div>
              <div className="seller-issues-stat-row">
                <div className="seller-issues-stat-card stat-card-resolved">
                  <div className="seller-issues-stat-number">
                    {issues.filter((i) => i.status === "resolved").length}
                  </div>
                  <div className="seller-issues-stat-label">Resolved</div>
                </div>
              </div>
              <div className="seller-issues-stat-divider"></div>
              <div className="seller-issues-stat-row">
                <div className="seller-issues-stat-card stat-card-unresolved">
                  <div className="seller-issues-stat-number">
                    {issues.filter((i) => i.status !== "resolved").length}
                  </div>
                  <div className="seller-issues-stat-label">Unresolved</div>
                </div>
              </div>
              <p className="seller-issues-stats-hint">Select a query to respond</p>
            </div>
          )}
        </aside>
      </div>
      </div>
    </div>
  );
}
