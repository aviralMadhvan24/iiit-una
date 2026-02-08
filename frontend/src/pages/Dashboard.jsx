import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import QuickSettings from "../components/QuickSettings";
import QuickNotifications from "../components/QuickNotifications";
import AppLayout from "../components/AppLayout";
import PageContainer from "../components/PageContainer";
import MetricCard from "../components/MetricCard";
import AlertItem from "../components/AlertItem";
import RiskChart from "../components/RiskCharts";
import { getAlertStats, getAlerts } from "../lib/api";

export default function Dashboard() {
  const navigate = useNavigate();

  const [wallet, setWallet] = useState(null);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isNotifOpen, setIsNotifOpen] = useState(false);

  const [stats, setStats] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    const storedWallet = localStorage.getItem("wallet");
    if (storedWallet) setWallet(storedWallet);

    async function loadData() {
      try {
        const statsRes = await getAlertStats();
        const alertsRes = await getAlerts({ limit: 5 });

        setStats(statsRes);
        setAlerts(alertsRes.alerts || []);

        // 🔥 APPEND NEW GRAPH POINT
        setChartData(prev => {
          const point = {
            time: new Date().toLocaleTimeString(),
            risk: Number((statsRes.avg_risk_score || 0) * 100).toFixed(1),
          };

          const updated = [...prev, point];

          // keep last 20 points
          return updated.slice(-20);
        });

      } catch (err) {
        console.error("Dashboard data fetch failed", err);
      }
    }

    loadData();
    const interval = setInterval(loadData, 5000); // every 5 sec

    return () => clearInterval(interval);
  }, []);

  return (
    <AppLayout
      headerProps={{
        onSettingsClick: () => setIsSettingsOpen(true),
        onNotifClick: () => setIsNotifOpen(true),
      }}
    >
      <PageContainer>

        {/* KPI Row */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">

          <MetricCard
            label="Connected Wallet"
            value={
              wallet
                ? <span title={wallet}>{wallet.slice(0, 6)}...{wallet.slice(-4)}</span>
                : "Not connected"
            }
            icon="account_balance_wallet"
            subtext="MetaMask"
            variant="secondary"
            onClick={() => wallet && navigator.clipboard.writeText(wallet)}
          />

          <MetricCard
            label="Total Transactions"
            value={stats ? stats.total_predictions : "--"}
            icon="receipt_long"
            subtext="+ live data"
            variant="primary"
          />

          <MetricCard
            label="High-Risk Detected"
            value={stats ? stats.total_alerts : "--"}
            icon="warning"
            subtext="Live alerts"
            variant="danger"
          />

          <MetricCard
            label="Avg. Risk Score"
            value={stats ? stats.avg_risk_score.toFixed(2) : "--"}
            icon="analytics"
            subtext="Model output"
            variant="secondary"
          />
        </div>

        {/* Analytics Section */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">

          {/* Graph */}
          <div className="lg:col-span-2 bg-surface-dark rounded-xl border border-[#283639] p-6">
            <h3 className="text-white text-xl font-bold mb-6">
              Real-time Risk Analysis
            </h3>
            <div className="h-[300px]">
              <RiskChart data={chartData} />
            </div>
          </div>

          {/* Alerts */}
          <div className="bg-surface-dark rounded-xl border border-[#283639] flex flex-col max-h-[500px]">
            <div className="p-4 border-b border-[#283639] bg-[#151c1e]">
              <h3 className="text-white text-lg font-bold">Live Alerts</h3>
            </div>

            <div className="overflow-y-auto p-4 space-y-3">
              {alerts.length === 0 && (
                <p className="text-gray-500 text-sm text-center">
                  No alerts detected
                </p>
              )}

              {alerts.map(alert => (
                <AlertItem
                  key={alert.id}
                  wallet={alert.wallet_address}
                  amount={`$${alert.amount_usd}`}
                  score={Math.round(alert.risk_score * 100)}
                  subtitle={alert.risk_level.toUpperCase()}
                  severity={alert.risk_level === "high" || alert.risk_level === "critical" ? "high" : "warning"}
                  time={new Date(alert.timestamp).toLocaleTimeString()}
                  onClick={() => navigate("/warning")}
                />
              ))}
            </div>
          </div>
        </div>

        <QuickSettings isOpen={isSettingsOpen} onClose={() => setIsSettingsOpen(false)} />
        <QuickNotifications isOpen={isNotifOpen} onClose={() => setIsNotifOpen(false)} />

      </PageContainer>
    </AppLayout>
  );
}
