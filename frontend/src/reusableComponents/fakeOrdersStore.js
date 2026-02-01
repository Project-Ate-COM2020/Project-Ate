
const KEY = "projectate_fake_orders_v1";

export function getFakeOrders() {
  try {
    const raw = localStorage.getItem(KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

export function addFakeOrder(order) {
  const orders = getFakeOrders();
  const next = [order, ...orders];
  localStorage.setItem(KEY, JSON.stringify(next));
  return next;
}

export function removeFakeOrder(orderId) {
    const orders = getFakeOrders();
    const next = orders.filter((o) => o.order_id !== orderId);
    localStorage.setItem(KEY, JSON.stringify(next));
    return next;
  }


export function makeClaimCode() {
  // Simple fake code generator like "ABCD-1234"
  const letters = "ABCDEFGHJKLMNPQRSTUVWXYZ";
  const part1 = Array.from({ length: 4 }, () => letters[Math.floor(Math.random() * letters.length)]).join("");
  const part2 = Math.floor(1000 + Math.random() * 9000);
  return `${part1}-${part2}`;
}