import { useNavigate } from "react-router-dom";

import AppLayout from "../components/AppLayout";
import PageContainer from "../components/PageContainer";
import GlassCard from "../components/GlassCard";
import PrimaryButton from "../components/PrimaryButton";
import SecondaryButton from "../components/SecondaryButton";

export default function AlertAction() {
  const navigate = useNavigate();

  return (
    <AppLayout
      headerProps={{
        title: "Alert Action Summary",
        showBack: false,
      }}
    >
      <PageContainer>

        <div className="flex items-center justify-center min-h-[70vh]">

          <GlassCard className="w-full max-w-3xl overflow-hidden border border-green-400/30">

            {/* ================= HEADER ================= */}
            <div className="p-8 text-center border-b border-white/5">
              <span className="material-symbols-outlined text-green-400 text-6xl">
                verified_user
              </span>

              <h2 className="text-3xl font-bold mt-4">
                Alert ID: #AL-9842
              </h2>

              <p className="text-red-400 font-bold mt-2">
                Risk Score: 94
              </p>
            </div>

            {/* ================= ACTION ================= */}
            <div className="p-8 bg-black/20">
              <p className="text-slate-400 text-sm uppercase tracking-widest mb-4">
                Action Taken
              </p>
              <p className="text-white font-medium">
                Escalated to Security Team
              </p>
            </div>

            {/* ================= NOTES ================= */}
            <div className="p-8 border-t border-white/5">
              <label className="block text-xs uppercase tracking-widest text-slate-500 mb-2">
                Analyst Notes
              </label>
              <textarea
                className="w-full bg-background-dark border border-white/10 rounded-lg p-4 text-sm text-slate-300 min-h-[120px]"
                placeholder="Additional mitigation notes..."
              />
            </div>

            {/* ================= ACTION BUTTONS ================= */}
            <div className="p-8 bg-black/40 flex flex-wrap gap-4 justify-between border-t border-white/5">

              <div className="flex gap-4">
                <PrimaryButton onClick={() => navigate("/dashboard")}>
                  <span className="material-symbols-outlined mr-2">
                    dashboard
                  </span>
                  Return to Dashboard
                </PrimaryButton>

                <SecondaryButton onClick={() => navigate("/warning")}>
                  <span className="material-symbols-outlined mr-2">
                    navigate_next
                  </span>
                  View Next Alert
                </SecondaryButton>
              </div>

              <button
                onClick={() => navigate("/forensic")}
                className="flex items-center gap-2 text-slate-400 hover:text-white"
              >
                <span className="material-symbols-outlined">
                  monitoring
                </span>
                Monitor Wallet Activity
              </button>

            </div>

          </GlassCard>

        </div>

      </PageContainer>
    </AppLayout>
  );
}
