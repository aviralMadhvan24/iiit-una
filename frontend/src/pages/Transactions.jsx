import React, { useEffect, useState } from "react";
import AppLayout from "../components/AppLayout";
import PageContainer from "../components/PageContainer";
import { getAlerts } from "../lib/api";

export default function Transactions() {
  const [poolTx, setPoolTx] = useState([]);
  const [completedTx, setCompletedTx] = useState([]);

  useEffect(() => {
    async function loadData() {
      try {
        const alertsRes = await getAlerts({ limit: 20 });

        const alerts = alertsRes.alerts || [];

        // 🔵 LIVE POOL (simulate incoming tx)
        setPoolTx(prev => {
          const incoming = alerts.slice(0, 5).map(tx => ({
            ...tx,
            status: "pending",
          }));

          return incoming;
        });

        // 🔴 COMPLETED / FLAGGED
        setCompletedTx(alerts);

      } catch (err) {
        console.error("Failed to load transactions", err);
      }
    }

    loadData();

    // 🔁 POLLING EVERY 4 SECONDS
    const interval = setInterval(loadData, 4000);

    return () => clearInterval(interval);
  }, []);

  return (
    <AppLayout headerProps={{ title: "Transaction Monitor" }}>
      <PageContainer>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

          {/* 🔵 LIVE POOL */}
          <div className="bg-surface-dark rounded-xl border border-[#283639] p-6">
            <h2 className="text-white text-xl font-bold mb-4">
              Live Pool (Incoming)
            </h2>

            <div className="space-y-3">
              {poolTx.length === 0 && (
                <p className="text-gray-500 text-sm">
                  Waiting for transactions...
                </p>
              )}

              {poolTx.map(tx => (
                <div
                  key={tx.id}
                  className="flex justify-between items-center bg-[#111718] border border-[#283639] rounded-lg p-4 animate-pulse"
                >
                  <div>
                    <p className="font-mono text-sm text-white">
                      {tx.wallet_address.slice(0, 10)}...
                    </p>
                    <p className="text-xs text-gray-500">
                      ${tx.amount_usd.toFixed(2)}
                    </p>
                  </div>

                  <span className="text-xs px-3 py-1 rounded-full bg-yellow-500/20 text-yellow-400 font-bold">
                    PENDING
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* 🔴 COMPLETED / FLAGGED */}
          <div className="bg-surface-dark rounded-xl border border-[#283639] p-6">
            <h2 className="text-white text-xl font-bold mb-4">
              Completed / Flagged
            </h2>

            <div className="space-y-3 max-h-[500px] overflow-y-auto">
              {completedTx.length === 0 && (
                <p className="text-gray-500 text-sm">
                  No processed transactions
                </p>
              )}

              {completedTx.map(tx => (
                <div
                  key={tx.id}
                  className="flex justify-between items-center bg-[#111718] border border-[#283639] rounded-lg p-4"
                >
                  <div>
                    <p className="font-mono text-sm text-white">
                      {tx.wallet_address.slice(0, 10)}...
                    </p>
                    <p className="text-xs text-gray-500">
                      ${tx.amount_usd.toFixed(2)}
                    </p>
                  </div>

                  <span
                    className={`text-xs px-3 py-1 rounded-full font-bold ${
                      tx.risk_level === "critical"
                        ? "bg-red-500/20 text-red-400"
                        : "bg-orange-500/20 text-orange-400"
                    }`}
                  >
                    {tx.risk_level.toUpperCase()}
                  </span>
                </div>
              ))}
            </div>
          </div>

        </div>

      </PageContainer>
    </AppLayout>
  );
}
