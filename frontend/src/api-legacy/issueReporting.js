import { requestJson } from "./authorisation";

const ISSUE_BASE = "/issues";

export async function createIssue({
  title,
  description,
  category,
  orderId,
  consumerId,
  posting,
  type,
}) {
  const resolvedConsumerId =
    consumerId ||
    localStorage.getItem("consumer_id") ||
    localStorage.getItem("consumerId") ||
    localStorage.getItem("buyerId") ||
    1;

  return requestJson(`${ISSUE_BASE}/report/`, {
    method: "POST",
    body: {
      consumer_id: resolvedConsumerId,
      posting: posting || orderId || null,
      type: type || category || title || "Other",
      description,
    },
  });
}

export async function fetchMyIssues(consumerId) {
  const resolvedConsumerId =
    consumerId ||
    localStorage.getItem("consumer_id") ||
    localStorage.getItem("consumerId") ||
    localStorage.getItem("buyerId") ||
    1;
  return requestJson(`${ISSUE_BASE}/buyer/${resolvedConsumerId}/`);
}

export async function fetchBuyerReportablePostings(consumerId) {
  const resolvedConsumerId =
    consumerId ||
    localStorage.getItem("consumer_id") ||
    localStorage.getItem("consumerId") ||
    localStorage.getItem("buyerId") ||
    1;
  return requestJson(`${ISSUE_BASE}/buyer/${resolvedConsumerId}/reportable-postings/`);
}

export async function fetchSellerIssues(sellerId) {
  return requestJson(`${ISSUE_BASE}/seller/${sellerId}/`);
}

export async function fetchSellerIssuesOverview(sellerId) {
  return requestJson(`${ISSUE_BASE}/seller/${sellerId}/overview/`);
}

export async function updateSellerIssue({ issueId, status, sellerResponse, sellerId }) {
  return requestJson(`${ISSUE_BASE}/seller/${sellerId}/${issueId}/respond/`, {
    method: "PATCH",
    body: {
      status: status || undefined,
      seller_response: sellerResponse || undefined,
    },
  });
}
