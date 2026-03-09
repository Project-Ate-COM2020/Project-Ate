import React, { useEffect, useState } from "react";
import NavBar from "../reusableComponents/navBar";
import { fetchSellerIssues, updateSellerIssue } from "../api-legacy/issueReporting";
import "./sellerIssuesPage.css";

const STATUS_OPTIONS = ["open", "responded", "resolved"];

export default function SellerIssuesPage() {
  const [issues, setIssues] = useState([
    {
      issue_id: 1,
      posting_id: 101,
      posting_category: "Bakery",
      consumer_name: "Sarah Johnson",
      consumer_id: 5,
      type: "Product quality",
      description: "The bread I received was stale and hard. It was not fresh at all. I expected fresh bakery items based on the listing description.",
      status: "open",
      seller_response: null,
      created_at: "2026-03-08T14:30:00",
    },
    {
      issue_id: 2,
      posting_id: 102,
      posting_category: "Vegetables",
      consumer_name: "Mike Chen",
      consumer_id: 12,
      type: "Order issue",
      description: "I ordered 2kg of tomatoes but only received 1kg. The package felt light when I picked it up.",
      status: "responded",
      seller_response: "I apologize for the mix-up. I've checked our records and found the error. We will provide a refund or replacement. Please let us know your preference.",
      created_at: "2026-03-07T10:15:00",
    },
    {
      issue_id: 3,
      posting_id: 103,
      posting_category: "Dairy",
      consumer_name: "Emma Wilson",
      consumer_id: 8,
      type: "Delivery issue",
      description: "The milk arrived 30 minutes after the pickup window ended. I had to wait much longer than expected.",
      status: "resolved",
      seller_response: "We sincerely apologize for the delay. This was due to traffic issues on that day. We've implemented better scheduling to prevent this in the future.",
      created_at: "2026-03-06T16:45:00",
    },
  ]);
  const [isLoadingIssues, setIsLoadingIssues] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  
  const [selectedIssueId, setSelectedIssueId] = useState(null);
  const [responseText, setResponseText] = useState("");
  const [statusValue, setStatusValue] = useState("open");
  const [isUpdating, setIsUpdating] = useState(false);
  
  // TODO: Get seller ID from session/auth context
  const sellerId = localStorage.getItem("sellerId") || "1";

  const loadIssues = async () => {
    setIsLoadingIssues(true);
    try {
      const data = await fetchSellerIssues(sellerId);
      setIssues(Array.isArray(data) ? data : []);
    } catch (err) {
      setIssues([]);
      setError("Failed to load issues");
    } finally {
      setIsLoadingIssues(false);
    }
  };

  useEffect(() => {
    // Uncomment to load real issues from backend
    // loadIssues();
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
      await updateSellerIssue({
        issueId: selectedIssueId,
        status: statusValue,
        sellerResponse: responseText.trim(),
        sellerId,
      });

      setSuccess("Issue updated successfully.");
      await loadIssues();
      handleClearSelection();
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

  return (
    <div className="seller-issues-page">
      <NavBar />
      <div className="seller-issues-container">
        <section className="seller-issues-list-panel">
          <h1 className="seller-issues-title">Customer Queries</h1>
          <p className="seller-issues-subtitle">Open queries from customers</p>

          {isLoadingIssues ? (
            <p className="seller-issues-empty-state">Loading issues...</p>
          ) : issues.length === 0 ? (
            <p className="seller-issues-empty-state">No open queries yet.</p>
          ) : (
            <div className="seller-issues-list">
              {issues.map((issue, index) => {
                const key = issue.issue_id || index;
                const displayConsumer = issue.consumer_name || "Unknown customer";
                const displayStatus = issue.status || "open";
                const displayType = issue.type || "General inquiry";
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
                          From: {displayConsumer}
                        </p>
                      </div>
                      <span className={`seller-issue-status-pill status-${displayStatus}`}>
                        {displayStatus}
                      </span>
                    </div>
                    <p className="seller-issue-card-category">
                      Category: {issue.posting_category || "Unknown"}
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
                    {currentIssue.consumer_name || "Unknown"}
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
                    {currentIssue.posting_category || "Unknown"}
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
  );
}
