import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import AppLayout from "../components/AppLayout";
import PageContainer from "../components/PageContainer";
import GlassCard from "../components/GlassCard";
import SecondaryButton from "../components/SecondaryButton";

import { getAlerts } from "../lib/api";

export default function Forensic() {
  const navigate = useNavigate();
  const [alert, setAlert] = useState(null);

  useEffect(() => {
    async function loadAlert() {
      try {
        const res = await getAlerts({ limit: 1 });
        if (res.alerts && res.alerts.length > 0) {
          setAlert(res.alerts[0]);
        }
      } catch (err) {
        console.error("Failed to load forensic data", err);
      }
    }

    loadAlert();
  }, []);

  return (
    <AppLayout
      headerProps={{
        title: "Wallet Forensics",
        showBack: true,
        backTo: "/warning",
        rightSlot: (
          <div className="flex items-center gap-3 text-xs font-mono">
            <span className="text-slate-400">Last Scanned:</span>
            <span className="text-white">Just now</span>
            <span className="w-3 h-3 bg-red-500 rounded-full animate-pulse" />
          </div>
        ),
      }}
    >
      <PageContainer>

        {/* ================= METRICS ================= */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">

          <GlassCard className="p-5">
            <p className="text-xs text-slate-400 uppercase">
              Total Transactions
            </p>
            <p className="text-3xl font-mono font-bold mt-2">
              {alert ? alert.alert_count || "—" : "—"}
            </p>
          </GlassCard>

          <GlassCard className="p-5">
            <p className="text-xs text-slate-400 uppercase">
              Average Tx Size
            </p>
            <p className="text-3xl font-mono font-bold mt-2">
              ${alert?.amount_usd ?? "--"}
            </p>
          </GlassCard>

          <GlassCard className="p-5">
            <p className="text-xs text-slate-400 uppercase">
              Historical Risk
            </p>
            <p className="text-xl font-bold text-yellow-400 mt-2">
              {alert?.risk_level?.toUpperCase() || "MODERATE"}
            </p>
          </GlassCard>

        </div>

        {/* ================= FLAGS TABLE ================= */}
        <GlassCard className="overflow-hidden">

          <div className="p-6 flex justify-between items-center border-b border-[#283639]">
            <h3 className="text-lg font-bold">
              Recent Behavioral Flags
            </h3>

            <SecondaryButton onClick={() => navigate("/review")}>
              View Full Report
            </SecondaryButton>
          </div>

          <table className="w-full text-sm">
            <tbody>

              <tr
                className="border-b border-[#283639] hover:bg-white/5 cursor-pointer"
                onClick={() => navigate("/review")}
              >
                <td className="p-4 font-mono text-slate-400">
                  {alert
                    ? new Date(alert.timestamp).toLocaleDateString()
                    : "--"}
                </td>

                <td className="p-4">
                  ML Anomaly Detected
                </td>

                <td className="p-4 text-red-400 font-bold">
                  {alert?.risk_level?.toUpperCase() || "HIGH"}
                </td>

                <td className="p-4 text-right">
                  <span className="material-symbols-outlined">
                    visibility
                  </span>
                </td>
              </tr>

              <tr
                className="border-b border-[#283639] hover:bg-white/5 cursor-pointer"
                onClick={() => navigate("/review")}
              >
                <td className="p-4 font-mono text-slate-400">
                  --
                </td>

                <td className="p-4">
                  Sudden Volume Spike
                </td>

                <td className="p-4 text-yellow-400 font-bold">
                  MED
                </td>

                <td className="p-4 text-right">
                  <span className="material-symbols-outlined">
                    visibility
                  </span>
                </td>
              </tr>

            </tbody>
          </table>

        </GlassCard>

        {/* ================= QUICK ACTION ================= */}
        <div className="flex justify-end mt-6">
          <SecondaryButton onClick={() => navigate("/action")}>
            Trigger Mitigation
          </SecondaryButton>
        </div>

      </PageContainer>
    </AppLayout>
  );
}
