import { useNavigate, useLocation } from "react-router-dom";
import { useEffect, useState } from "react";

const API_BASE = "http://localhost:8000/api/v1";

export default function Header({
  title = "Suraksha Chain",
  onSettingsClick,
  onNotifClick,
}) {
  const navigate = useNavigate();
  const location = useLocation();

  const [wallet, setWallet] = useState(null);
  const [poolRunning, setPoolRunning] = useState(false);
  const [loading, setLoading] = useState(false);

  // ======================
  // INIT
  // ======================
  useEffect(() => {
    const storedWallet = localStorage.getItem("wallet");
    if (storedWallet) setWallet(storedWallet);
  }, []);

  useEffect(() => {
    fetchPoolStatus();
  }, []);

  // ======================
  // API CALLS
  // ======================
  async function fetchPoolStatus() {
    try {
      const res = await fetch(`${API_BASE}/simulator/status`);
      const data = await res.json();
      setPoolRunning(data.running);
    } catch (e) {
      console.error("❌ Failed to fetch pool status", e);
    }
  }

  async function startPool() {
    setLoading(true);
    await fetch(`${API_BASE}/simulator/start`, { method: "POST" });
    await fetchPoolStatus();
    setLoading(false);
  }

  async function stopPool() {
    setLoading(true);
    await fetch(`${API_BASE}/simulator/stop`, { method: "POST" });
    await fetchPoolStatus();
    setLoading(false);
  }

  async function resetPool() {
    const ok = window.confirm(
      "This will clear ALL transactions and alerts.\nContinue?",
    );
    if (!ok) return;

    setLoading(true);
    await fetch(`${API_BASE}/simulator/reset`, { method: "POST" });
    await fetchPoolStatus();
    setLoading(false);
  }

  // ======================
  // UI HELPERS
  // ======================
  const shortWallet = wallet
    ? `${wallet.slice(0, 6)}...${wallet.slice(-4)}`
    : "Not connected";

  const isTransactionsActive = location.pathname === "/transactions";

  // ======================
  // RENDER
  // ======================
  return (
    <header className="flex items-center justify-between border-b border-[#283639] px-6 py-4 bg-[#111718] sticky top-0 z-50 font-display">
      {/* LEFT */}
      <div
        className="flex items-center gap-4 text-white cursor-pointer"
        onClick={() => navigate("/dashboard")}
      >
        <span className="material-symbols-outlined text-primary text-[32px]">
          shield_lock
        </span>
        <h2 className="text-2xl font-bold tracking-tight">{title}</h2>
      </div>

      {/* CENTER */}
      <div className="hidden md:flex items-center gap-4">
        {/* Network */}
        <div className="flex items-center gap-2 px-4 py-2 bg-surface-dark rounded-full border border-[#283639]">
          <span className="material-symbols-outlined text-gray-400 text-sm">
            token
          </span>
          <span className="text-sm font-medium text-white">
            Sepolia Testnet
          </span>
        </div>

        {/* Transactions */}
        <button
          onClick={() => navigate("/transactions")}
          className={`flex items-center gap-2 px-4 py-2 rounded-full border transition-colors ${
            isTransactionsActive
              ? "bg-primary/20 border-primary text-primary"
              : "bg-surface-dark border-[#283639] text-white hover:bg-[#283639]"
          }`}
        >
          <span className="material-symbols-outlined text-sm">sync_alt</span>
          <span className="text-sm font-medium">Transactions</span>
        </button>

        {/* Wallet Activity */}
        <button
          onClick={() => navigate("/wallet-activity")}
          className="flex items-center gap-2 px-4 py-2 rounded-full border bg-surface-dark border-[#283639] text-white hover:bg-[#283639]"
        >
          <span className="material-symbols-outlined text-sm">
            account_balance_wallet
          </span>
          <span className="text-sm font-medium">My Wallet</span>
        </button>

        {/* ========================= */}
        {/* 🔥 SIMULATOR CONTROLS */}
        {/* ========================= */}
        <div className="flex items-center gap-2 px-3 py-2 bg-surface-dark rounded-full border border-[#283639]">
          <span className="text-xs text-gray-400">Pool</span>

          <span
            className={`text-xs font-bold ${
              poolRunning ? "text-green-400" : "text-red-400"
            }`}
          >
            {poolRunning ? "LIVE" : "STOPPED"}
          </span>

          {!poolRunning ? (
            <button
              onClick={startPool}
              disabled={loading}
              className="text-xs px-2 py-1 rounded bg-green-600 hover:bg-green-500 text-white"
            >
              Start
            </button>
          ) : (
            <button
              onClick={stopPool}
              disabled={loading}
              className="text-xs px-2 py-1 rounded bg-red-600 hover:bg-red-500 text-white"
            >
              Stop
            </button>
          )}

          {/* 🧹 RESET */}
          <button
            onClick={resetPool}
            disabled={loading}
            className="text-xs px-2 py-1 rounded bg-yellow-600 hover:bg-yellow-500 text-black font-semibold"
          >
            Reset
          </button>
        </div>
      </div>

      {/* RIGHT */}
      <div className="flex items-center gap-4">
        {/* Notifications */}
        <button
          onClick={onNotifClick}
          className="relative flex items-center justify-center rounded-lg h-10 px-4 bg-surface-dark border border-[#283639] hover:bg-[#283639] text-white"
        >
          <span className="material-symbols-outlined text-[20px]">
            notifications
          </span>
          <div className="absolute top-2 right-3 size-2 rounded-full bg-accent-red"></div>
        </button>

        {/* Settings */}
        <button
          onClick={onSettingsClick}
          className="flex items-center justify-center rounded-lg h-10 px-4 bg-surface-dark border border-[#283639] hover:bg-[#283639] text-white"
        >
          <span className="material-symbols-outlined text-[20px]">
            settings
          </span>
        </button>

        {/* Wallet */}
        <div
          onClick={() => navigate("/profile")}
          className="flex items-center gap-3 pl-4 border-l border-[#283639] cursor-pointer group"
        >
          <div className="text-right hidden sm:block">
            <div className="text-[10px] text-primary font-bold uppercase">
              {wallet ? "Connected" : "Disconnected"}
            </div>
            <div
              className="text-sm font-mono text-gray-400 group-hover:text-white"
              title={wallet || ""}
            >
              {shortWallet}
            </div>
          </div>

          <div className="bg-gradient-to-br from-primary to-purple-600 rounded-full p-0.5">
            <div className="bg-surface-dark rounded-full p-1">
              <span className="material-symbols-outlined text-white text-sm">
                wallet
              </span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
