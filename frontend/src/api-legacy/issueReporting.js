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
