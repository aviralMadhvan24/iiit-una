import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import QuickSettings from "../components/QuickSettings";
import QuickNotifications from "../components/QuickNotifications";
import AppLayout from "../components/AppLayout";
import PageContainer from "../components/PageContainer";
import MetricCard from "../components/MetricCard";
import AlertItem from "../components/AlertItem";

import { getAlertStats, getAlerts } from "../lib/api";

export default function Dashboard() {
  const navigate = useNavigate();

  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isNotifOpen, setIsNotifOpen] = useState(false);

  const [stats, setStats] = useState(null);
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    async function loadData() {
      try {
        const statsRes = await getAlertStats();
        const alertsRes = await getAlerts({ limit: 5 });

        setStats(statsRes);
        setAlerts(alertsRes.alerts || []);
      } catch (err) {
        console.error("Dashboard data fetch failed", err);
      }
    }

    loadData();
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
            trendIcon="arrow_outward"
          />

          <MetricCard
            label="Avg. Risk Score"
            value={stats ? stats.avg_risk_score.toFixed(2) : "--"}
            icon="analytics"
            subtext="Model output"
            variant="secondary"
            trendIcon="trending_down"
          />

          <div className="bg-surface-dark border border-[#283639] rounded-xl p-5 relative flex flex-col justify-between overflow-hidden group">
            <span className="material-symbols-outlined text-6xl absolute right-0 top-0 opacity-10 p-2 text-accent-green">
              shield
            </span>

            <div>
              <p className="text-gray-400 text-sm font-medium mb-1">
                Current Threat Level
              </p>

              <div className="flex items-center gap-3 mt-2">
                <h3 className="text-white text-3xl font-bold tracking-tight">
                  {stats && stats.alert_rate > 0.05 ? "ELEVATED" : "LOW"}
                </h3>

                <div className="relative flex h-3 w-3">
                  <span className="animate-ping absolute h-full w-full rounded-full bg-accent-green opacity-75"></span>
                  <span className="relative h-3 w-3 bg-accent-green rounded-full shadow-[0_0_10px_#0bda54]"></span>
                </div>
              </div>
            </div>

            <p className="text-accent-green text-sm font-medium mt-4">
              System Stable
            </p>
          </div>
        </div>

        {/* Analytics Section */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">

          {/* Graph section untouched */}
          <div className="lg:col-span-2 bg-surface-dark rounded-xl border border-[#283639] p-6 flex flex-col">
            <h3 className="text-white text-xl font-bold mb-6">
              Real-time Risk Analysis
            </h3>
            <div className="h-[300px] flex items-center justify-center text-gray-500">
              Graph Placeholder
            </div>
          </div>

          {/* Live Alerts */}
          <div className="bg-surface-dark rounded-xl border border-[#283639] flex flex-col max-h-[500px]">
            <div className="p-4 border-b border-[#283639] bg-[#151c1e] rounded-t-xl">
              <h3 className="text-white text-lg font-bold">
                Live Alerts
              </h3>
            </div>

            <div className="overflow-y-auto p-4 space-y-3 custom-scrollbar">
              {alerts.length === 0 && (
                <p className="text-gray-500 text-sm text-center">
                  No alerts detected
                </p>
              )}

              {alerts.map((alert) => (
                <AlertItem
                  key={alert.id}
                  wallet={alert.wallet_address}
                  amount={`$${alert.amount_usd}`}
                  score={Math.round(alert.risk_score * 100)}
                  subtitle={alert.risk_level.toUpperCase()}
                  severity={
                    alert.risk_level === "high" ||
                    alert.risk_level === "critical"
                      ? "high"
                      : "warning"
                  }
                  time={new Date(alert.timestamp).toLocaleTimeString()}
                  onClick={() => navigate("/warning")}
                />
              ))}
            </div>
          </div>
        </div>

        {/* Overlay Components */}
        <QuickSettings
          isOpen={isSettingsOpen}
          onClose={() => setIsSettingsOpen(false)}
        />

        <QuickNotifications
          isOpen={isNotifOpen}
          onClose={() => setIsNotifOpen(false)}
        />
      </PageContainer>
    </AppLayout>
  );
}
