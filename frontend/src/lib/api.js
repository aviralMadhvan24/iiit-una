const BASE_URL =
  import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";

/* ================= CORE FETCH WRAPPER ================= */
async function apiRequest(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
    },
    ...options,
  });

  const data = await res.json().catch(() => null);

  if (!res.ok) {
    const error = new Error(data?.detail || "API request failed");
    error.status = res.status;
    error.data = data;
    throw error; // 🔥 DO NOT CATCH HERE
  }

  return data;
}


/* ================= HEALTH ================= */
export const getHealth = () => apiRequest("/health");
export const getReadiness = () => apiRequest("/health/ready");

/* ================= PREDICTION ================= */
export const predictTransaction = (payload) =>
  apiRequest("/predict", {
    method: "POST",
    body: JSON.stringify(payload),
  });

export const batchPredict = (transactions) =>
  apiRequest("/predict/batch", {
    method: "POST",
    body: JSON.stringify({ transactions }),
  });

export const getModelInfo = () => apiRequest("/predict/model-info");

/* ================= ALERTS ================= */
export const getAlerts = (params = {}) => {
  const query = new URLSearchParams(params).toString();
  return apiRequest(`/alerts${query ? `?${query}` : ""}`);
};

export const getAlertById = (id) => apiRequest(`/alerts/${id}`);

export const verifyAlert = (id, body) =>
  apiRequest(`/alerts/${id}/verify`, {
    method: "POST",
    body: JSON.stringify(body),
  });

export const getAlertStats = () => apiRequest("/alerts/stats");

/* ================= DEFAULT EXPORT ================= */
export default {
  request: apiRequest,   // ✅ THIS LINE FIXES EVERYTHING
  getHealth,
  getReadiness,
  predictTransaction,
  batchPredict,
  getModelInfo,
  getAlerts,
  getAlertById,
  verifyAlert,
  getAlertStats,
};
