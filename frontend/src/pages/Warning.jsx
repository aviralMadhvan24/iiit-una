import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import AppLayout from "../components/AppLayout";
import PageContainer from "../components/PageContainer";
import GlassCard from "../components/GlassCard";
import PrimaryButton from "../components/PrimaryButton";
import SecondaryButton from "../components/SecondaryButton";

import { getAlerts } from "../lib/api";

export default function Warning() {
  const navigate = useNavigate();
  const [alert, setAlert] = useState(null);

  useEffect(() => {
    async function loadAlert() {
      try {
        // Fetch most recent alert
        const res = await getAlerts({ limit: 1 });
        if (res.alerts && res.alerts.length > 0) {
          setAlert(res.alerts[0]);
        }
      } catch (err) {
        console.error("Failed to load alert", err);
      }
    }

    loadAlert();
  }, []);

  return (
    <AppLayout
      headerProps={{
        title: "Alert Investigation",
        showBack: true,
        backTo: "/dashboard",
        rightSlot: (
          <div className="text-xs font-mono text-slate-400">
            Alert ID:{" "}
            <span className="text-red-400 font-bold">
              #{alert ? alert.id : "--"}
            </span>
          </div>
        ),
      }}
    >
      <PageContainer>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">

          {/* ================= LEFT ================= */}
          <div className="col-span-12 lg:col-span-7 flex flex-col gap-6">

            {/* TRANSACTION DETAILS */}
            <GlassCard
              className="p-6 cursor-pointer hover:bg-white/5 transition"
              onClick={() => navigate("/forensic")}
            >
              <h2 className="text-lg font-bold mb-4 flex items-center gap-2">
                <span className="material-symbols-outlined text-primary">
                  receipt_long
                </span>
                Transaction Details
              </h2>

              <div className="grid grid-cols-2 gap-6">
                <div>
                  <p className="text-xs text-slate-400">
                    Transaction Hash
                  </p>
                  <p className="font-mono text-lg">
                    {alert?.tx_hash || "--"}
                  </p>
                </div>

                <div>
                  <p className="text-xs text-slate-400">Block</p>
                  <p className="font-mono text-lg">
                    --
                  </p>
                </div>

                <div>
                  <p className="text-xs text-slate-400">
                    From Wallet
                  </p>
                  <p className="font-mono">
                    {alert?.wallet_address || "--"}
                  </p>
                </div>

                <div>
                  <p className="text-xs text-slate-400">
                    Protocol
                  </p>
                  <p className="font-mono">
                    DeFi Protocol
                  </p>
                </div>
              </div>

              <div className="mt-6 flex justify-between items-center">
                <div>
                  <p className="text-xs text-slate-400">
                    Value
                  </p>
                  <p className="text-3xl font-bold">
                    ${alert?.amount_usd ?? "--"}
                  </p>
                </div>

                <span className="px-3 py-1 bg-yellow-500/10 border border-yellow-500/30 rounded text-yellow-400 text-xs font-bold">
                  WHALE TX
                </span>
              </div>
            </GlassCard>

          </div>

          {/* ================= RIGHT ================= */}
          <div className="col-span-12 lg:col-span-5">
            <GlassCard className="p-6 border-t-4 border-red-500">
              <h2 className="text-lg font-bold mb-6 flex items-center gap-2">
                <span className="material-symbols-outlined text-red-400">
                  gpp_maybe
                </span>
                Risk Analysis
              </h2>

              <div className="text-center">
                <p className="text-5xl font-bold text-red-400">
                  {alert ? Math.round(alert.risk_score * 100) : "--"}
                  <span className="text-2xl">/100</span>
                </p>

                <p className="text-sm text-red-400 font-bold mt-2 uppercase">
                  {alert?.risk_level || "CRITICAL"} Risk
                </p>
              </div>

              <ul className="mt-6 space-y-3 text-sm text-slate-300">
                <li>• Abnormal transaction size</li>
                <li>• Behavioral anomaly detected</li>
                <li>• ML-based risk escalation</li>
              </ul>
            </GlassCard>
          </div>

        </div>

        {/* ================= FOOTER ACTIONS ================= */}
        <div className="flex justify-end gap-4 mt-6">
          <SecondaryButton onClick={() => navigate("/review")}>
            Mark as Reviewed
          </SecondaryButton>

          <PrimaryButton onClick={() => navigate("/action")}>
            Trigger Mitigation
          </PrimaryButton>
        </div>

      </PageContainer>
    </AppLayout>
  );
}
