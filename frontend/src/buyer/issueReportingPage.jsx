import React, { useEffect, useState } from "react";
import NavBar from "../reusableComponents/navBar";
import { getData, postData } from "../reusableComponents/api";
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
  const [selectedPostingId, setSelectedPostingId] = useState("");
  const [reportableOrders, setReportableOrders] = useState([]);
  const [isLoadingOrders, setIsLoadingOrders] = useState(true);

  const [issues, setIssues] = useState([]);
  const [isLoadingIssues, setIsLoadingIssues] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const formatIssueType = (value) =>
    String(value || "Issue")
      .replace(/_/g, " ")
      .replace(/\b\w/g, (char) => char.toUpperCase());

  const loadIssues = async () => {
    setIsLoadingIssues(true);
    try {
      const data = await getData("issues/consumer/");
      const parsedIssues = Array.isArray(data)
        ? data
        : Array.isArray(data?.results)
          ? data.results
          : [];
      setIssues(parsedIssues);
    } catch {
      setIssues([]);
    } finally {
      setIsLoadingIssues(false);
    }
  };

  const loadReportableOrders = async () => {
    setIsLoadingOrders(true);
    try {
      const data = await getData("issues/consumer/reportable");
      const orders = Array.isArray(data) ? data : [];
      setReportableOrders(orders);

      if (orders.length > 0) {
        setSelectedPostingId(String(orders[0].posting_id));
      } else {
        setSelectedPostingId("");
      }
    } catch {
      setReportableOrders([]);
      setSelectedPostingId("");
    } finally {
      setIsLoadingOrders(false);
    }
  };

  useEffect(() => {
    loadIssues();
    loadReportableOrders();
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setSuccess("");
    setIsLoading(true);

    try {
      const payloadDescription = title.trim()
        ? `${title.trim()} - ${description.trim()}`
        : description.trim();

      const response = await postData("issues/report/", {
        posting: Number(selectedPostingId),
        type: category,
        description: payloadDescription,
      });

      if (response?.error) {
        throw new Error(response.error);
      }

      setSuccess("Issue submitted successfully.");
      setTitle("");
      setDescription("");
      setCategory(CATEGORY_OPTIONS[0]);
      if (reportableOrders.length > 0) {
        setSelectedPostingId(String(reportableOrders[0].posting_id));
      } else {
        setSelectedPostingId("");
      }
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
    <div className="buyer-page issue-dashboard-page">
      <NavBar />
      <section className="buyer-hero">
        <p className="buyer-hero-label">Support</p>
        <h1 className="buyer-hero-title">Issue Dashboard</h1>
        <p className="buyer-hero-subtitle">Track your reports and submit new issues in one place.</p>
      </section>
      <div className="buyer-container issue-dashboard-container">
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
                const displayTitle = formatIssueType(issue.type);
                const displayCategory = issue.posting?.category || "Uncategorised";
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
                className="buyer-input issue-input"
                value={title}
                onChange={(event) => setTitle(event.target.value)}
                placeholder="Short summary of the issue"
                required
              />
            </label>

            <label className="issue-label">
              Category
              <select
                className="buyer-input issue-input"
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
              Select Order
              <select
                className="buyer-input issue-input"
                value={selectedPostingId}
                onChange={(event) => setSelectedPostingId(event.target.value)}
                required
                disabled={isLoadingOrders || reportableOrders.length === 0}
              >
                {isLoadingOrders ? (
                  <option value="">Loading orders...</option>
                ) : reportableOrders.length === 0 ? (
                  <option value="">No eligible orders found</option>
                ) : (
                  reportableOrders.map((order) => (
                    <option key={order.posting_id} value={String(order.posting_id)}>
                      #{order.posting_id} - {order.category || "Unknown category"} - {order.pickup_window || "No pickup window"}
                    </option>
                  ))
                )}
              </select>
            </label>

            <label className="issue-label">
              Description
              <textarea
                className="buyer-input issue-input issue-textarea"
                value={description}
                onChange={(event) => setDescription(event.target.value)}
                placeholder="Describe the issue in detail"
                rows={6}
                required
              />
            </label>

            <button
              className="buyer-btn-primary issue-submit-btn"
              disabled={isLoading || isLoadingOrders || reportableOrders.length === 0 || !selectedPostingId}
            >
              {isLoading ? "Submitting..." : "Submit issue"}
            </button>
          </form>
        </aside>
        </div>
      </div>
  );
}
