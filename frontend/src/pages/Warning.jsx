import { useNavigate } from "react-router-dom";

import AppLayout from "../components/AppLayout";
import PageContainer from "../components/PageContainer";
import GlassCard from "../components/GlassCard";
import PrimaryButton from "../components/PrimaryButton";
import SecondaryButton from "../components/SecondaryButton";

export default function Warning() {
  const navigate = useNavigate();

  return (
    <AppLayout
      headerProps={{
        title: "Alert Investigation",
        showBack: true,
        backTo: "/dashboard",
        rightSlot: (
          <div className="text-xs font-mono text-slate-400">
            Alert ID: <span className="text-red-400 font-bold">#AL-9842</span>
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
                    0x84a...2f1
                  </p>
                </div>

                <div>
                  <p className="text-xs text-slate-400">Block</p>
                  <p className="font-mono text-lg">
                    18,452,994
                  </p>
                </div>

                <div>
                  <p className="text-xs text-slate-400">
                    From Wallet
                  </p>
                  <p className="font-mono">
                    0x71c...8e4
                  </p>
                </div>

                <div>
                  <p className="text-xs text-slate-400">
                    Protocol
                  </p>
                  <p className="font-mono">
                    Aave V3
                  </p>
                </div>
              </div>

              <div className="mt-6 flex justify-between items-center">
                <div>
                  <p className="text-xs text-slate-400">
                    Value
                  </p>
                  <p className="text-3xl font-bold">
                    $4.5M
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
                  94
                  <span className="text-2xl">/100</span>
                </p>
                <p className="text-sm text-red-400 font-bold mt-2 uppercase">
                  Critical Risk
                </p>
              </div>

              <ul className="mt-6 space-y-3 text-sm text-slate-300">
                <li>• Abnormal transaction size</li>
                <li>• Flash loan interaction</li>
                <li>• Rapid liquidity removal</li>
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
