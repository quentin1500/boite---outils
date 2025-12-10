const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

export async function fetchTools({ q, category_id, tag } = {}) {
  const params = new URLSearchParams();
  if (q) params.append("q", q);
  if (category_id) params.append("category_id", category_id);
  if (tag) params.append("tag", tag);
  const res = await fetch(`${API_BASE}/tools?${params.toString()}`);
  return res.json();
}

export async function createTool(payload) {
  const res = await fetch(`${API_BASE}/tools`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(payload)
  });
  return res.json();
}

export async function fetchCategories() {
  const res = await fetch(`${API_BASE}/categories`);
  return res.json();
}

export async function fetchTags() {
  const res = await fetch(`${API_BASE}/tags`);
  return res.json();
}
