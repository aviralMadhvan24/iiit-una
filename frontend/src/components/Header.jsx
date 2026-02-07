import { useNavigate, useLocation } from "react-router-dom";
import { useEffect, useState } from "react";

export default function Header({
  title = "Sentinel AI",
  onSettingsClick,
  onNotifClick,
}) {
  const navigate = useNavigate();
  const location = useLocation();

  const [wallet, setWallet] = useState(null);

  useEffect(() => {
    const storedWallet = localStorage.getItem("wallet");
    if (storedWallet) {
      setWallet(storedWallet);
    }
  }, []);

  const shortWallet = wallet
    ? `${wallet.slice(0, 6)}...${wallet.slice(-4)}`
    : "Not connected";

  const isTransactionsActive = location.pathname === "/transactions";

  return (
    <header className="flex items-center justify-between border-b border-[#283639] px-6 py-4 bg-[#111718] sticky top-0 z-50 font-display">
      
      {/* LEFT: Brand */}
      <div
        className="flex items-center gap-4 text-white cursor-pointer"
        onClick={() => navigate("/dashboard")}
      >
        <span className="material-symbols-outlined text-primary text-[32px]">
          shield_lock
        </span>
        <h2 className="text-2xl font-bold tracking-tight">
          {title}
        </h2>
      </div>

      {/* CENTER: Network + Nav */}
      <div className="hidden md:flex items-center gap-4">
        
        {/* Network */}
        <div className="flex items-center gap-2 px-4 py-2 bg-surface-dark rounded-full border border-[#283639]">
          <span className="material-symbols-outlined text-gray-400 text-sm">
            token
          </span>
          <span className="text-sm font-medium text-white">
            Ethereum Mainnet
          </span>
          <span className="material-symbols-outlined text-gray-400 text-sm">
            expand_more
          </span>
        </div>

        {/* Transactions Nav */}
        <button
          onClick={() => navigate("/transactions")}
          className={`flex items-center gap-2 px-4 py-2 rounded-full border transition-colors
            ${
              isTransactionsActive
                ? "bg-primary/20 border-primary text-primary"
                : "bg-surface-dark border-[#283639] text-white hover:bg-[#283639]"
            }
          `}
        >
          <span className="material-symbols-outlined text-sm">
            sync_alt
          </span>
          <span className="text-sm font-medium">
            Transactions
          </span>
        </button>
      </div>

      {/* RIGHT: Actions + Wallet */}
      <div className="flex items-center gap-4">

        {/* Notifications */}
        <button
          onClick={onNotifClick}
          className="relative flex items-center justify-center rounded-lg h-10 px-4 bg-surface-dark border border-[#283639] hover:bg-[#283639] text-white transition-colors"
        >
          <span className="material-symbols-outlined text-[20px]">
            notifications
          </span>
          <div className="absolute top-2 right-3 size-2 rounded-full bg-accent-red"></div>
        </button>

        {/* Settings */}
        <button
          onClick={onSettingsClick}
          className="flex items-center justify-center rounded-lg h-10 px-4 bg-surface-dark border border-[#283639] hover:bg-[#283639] text-white transition-colors"
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
              className="text-sm font-mono text-gray-400 group-hover:text-white transition-colors"
              title={wallet || ""}
            >
              {shortWallet}
            </div>
          </div>

          <div className="bg-gradient-to-br from-primary to-purple-600 rounded-full p-0.5 shadow-neon group-hover:scale-105 transition-transform">
            <div className="bg-surface-dark rounded-full p-1 flex">
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
