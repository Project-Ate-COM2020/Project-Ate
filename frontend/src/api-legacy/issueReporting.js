import { requestJson } from "./authorisation";

const ISSUE_BASE = "/issue-reporting";

export async function createIssue({ title, description, category, orderId }) {
  return requestJson(`${ISSUE_BASE}/issues/`, {
    method: "POST",
    body: {
      title,
      description,
      category,
      order_id: orderId || null,
    },
  });
}

export async function fetchMyIssues() {
  return requestJson(`${ISSUE_BASE}/issues/mine/`);
}

export async function fetchSellerIssues(sellerId) {
  return requestJson(`/seller/issues/?seller_id=${sellerId}`);
}

export async function updateSellerIssue({ issueId, status, sellerResponse, sellerId }) {
  return requestJson(`/seller/issues/update/?seller_id=${sellerId}`, {
    method: "POST",
    body: {
      issue_id: issueId,
      status: status || undefined,
      seller_response: sellerResponse || undefined,
    },
  });
}
