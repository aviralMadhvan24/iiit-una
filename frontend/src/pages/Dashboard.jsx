import { useNavigate } from "react-router-dom";

import AppLayout from "../components/AppLayout";
import PageContainer from "../components/PageContainer";
import MetricCard from "../components/MetricCard";
import AlertItem from "../components/AlertItem";
import GlassCard from "../components/GlassCard";

export default function Dashboard() {
  const navigate = useNavigate();

  return (
    <AppLayout
      headerProps={{
        title: "Sentinel AI",
        showBack: false,
      }}
    >
      <PageContainer>

        {/* ================= KPI CARDS ================= */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <MetricCard
            label="Total Transactions"
            value="1.2M"
            icon="receipt_long"
            accent="text-primary"
            subtext="+2.4% vs last week"
          />

          <MetricCard
            label="High-Risk Detected"
            value="14"
            icon="warning"
            accent="text-red-400"
            subtext="+12% spike today"
          />

          <MetricCard
            label="Avg. Risk Score"
            value="18"
            icon="analytics"
            accent="text-secondary"
            subtext="-5% improvement"
          />

          <MetricCard
            label="Current Threat Level"
            value="LOW"
            icon="shield"
            accent="text-green-400"
            subtext="System Stable"
          />
        </div>

        {/* ================= MAIN GRID ================= */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">

          {/* ======== RISK CHART (STATIC SVG as-is) ======== */}
          <GlassCard className="lg:col-span-2 p-6">
            <div className="flex justify-between items-center mb-6">
              <div>
                <h3 className="text-xl font-bold flex items-center gap-2">
                  <span className="material-symbols-outlined text-primary">
                    monitoring
                  </span>
                  Real-time Risk Analysis
                </h3>
                <p className="text-sm text-gray-400">
                  Global network risk score fluctuations
                </p>
              </div>

              <div className="flex gap-2">
                <button className="px-3 py-1 bg-[#283639] text-xs rounded">
                  1H
                </button>
                <button className="px-3 py-1 bg-primary text-black text-xs font-bold rounded">
                  24H
                </button>
                <button className="px-3 py-1 bg-[#283639] text-xs rounded">
                  7D
                </button>
              </div>
            </div>

            {/* SVG kept exactly (no React chart yet) */}
            <div className="w-full h-[300px]">
              <svg viewBox="0 0 800 300" className="w-full h-full">
                <path
                  d="M0,220 Q100,200 200,230 T400,180 T600,120 T800,150"
                  fill="none"
                  stroke="#0dccf2"
                  strokeWidth="3"
                />
              </svg>
            </div>
          </GlassCard>

          {/* ======== LIVE ALERT FEED ======== */}
          <GlassCard className="p-4 flex flex-col max-h-[450px]">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-bold">Live Alerts</h3>
              <span className="text-xs text-gray-500">Real-time</span>
            </div>

            <div className="flex flex-col gap-3 overflow-y-auto">
              <AlertItem
                wallet="0x71C...8e4"
                amount="$420,000"
                score={88}
                subtitle="Suspicious transfer pattern"
                onClick={() => navigate("/warning")}
              />

              <AlertItem
                wallet="0x3A2...b99"
                amount="$85,200"
                score={65}
                subtitle="Flash loan detected"
                onClick={() => navigate("/warning")}
              />

              <AlertItem
                wallet="0x99B...c21"
                amount="$12,050"
                score={52}
                subtitle="Unverified contract interaction"
                onClick={() => navigate("/warning")}
              />
            </div>
          </GlassCard>
        </div>

        {/* ================= TRANSACTION TABLE ================= */}
        <GlassCard className="overflow-hidden">
          <div className="p-6 border-b border-[#283639] flex justify-between items-center">
            <h3 className="text-xl font-bold">Recent Transactions</h3>

            <input
              placeholder="Search hash or wallet..."
              className="bg-[#111718] border border-[#283639] rounded-lg px-4 py-2 text-sm"
            />
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-[#151c1e] text-gray-400">
                <tr>
                  <th className="px-6 py-4 text-left">Timestamp</th>
                  <th className="px-6 py-4 text-left">Wallet</th>
                  <th className="px-6 py-4 text-left">Type</th>
                  <th className="px-6 py-4 text-left">Amount</th>
                  <th className="px-6 py-4 text-center">Risk</th>
                </tr>
              </thead>

              <tbody className="divide-y divide-[#283639]">
                <tr
                  className="hover:bg-[#1c2628] cursor-pointer"
                  onClick={() => navigate("/warning")}
                >
                  <td className="px-6 py-4 text-gray-400">2m ago</td>
                  <td className="px-6 py-4 font-mono text-primary">
                    0x71C...8e4
                  </td>
                  <td className="px-6 py-4">Token Transfer</td>
                  <td className="px-6 py-4 font-bold">$420,000</td>
                  <td className="px-6 py-4 text-center text-red-400 font-bold">
                    88
                  </td>
                </tr>

                <tr className="hover:bg-[#1c2628]">
                  <td className="px-6 py-4 text-gray-400">5m ago</td>
                  <td className="px-6 py-4 font-mono">0x92A...b12</td>
                  <td className="px-6 py-4">Swap</td>
                  <td className="px-6 py-4 font-bold">$15,000</td>
                  <td className="px-6 py-4 text-center text-green-400 font-bold">
                    12
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </GlassCard>

      </PageContainer>
    </AppLayout>
  );
}
