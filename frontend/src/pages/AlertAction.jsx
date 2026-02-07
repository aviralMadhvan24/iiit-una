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
        title: "Mitigation Actions",
        showBack: true,
        backTo: "/dashboard",
      }}
    >
      <PageContainer>

        {/* ================= ACTION SUMMARY ================= */}
        <GlassCard className="p-6 mb-6">
          <h2 className="text-xl font-bold mb-4 flex items-center gap-2">
            <span className="material-symbols-outlined text-red-400">
              gavel
            </span>
            Threat Response Initiated
          </h2>

          <p className="text-slate-300 leading-relaxed">
            The alert has been successfully reviewed and logged.
            Mitigation actions can now be initiated to prevent
            further exposure or loss.
          </p>
        </GlassCard>

        {/* ================= ACTION OPTIONS ================= */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

          <GlassCard className="p-6 cursor-pointer hover:bg-white/5 transition">
            <h3 className="text-lg font-bold mb-2 flex items-center gap-2">
              <span className="material-symbols-outlined text-yellow-400">
                lock
              </span>
              Freeze Wallet
            </h3>

            <p className="text-sm text-slate-400">
              Temporarily suspend transactions originating
              from the flagged wallet address.
            </p>
          </GlassCard>

          <GlassCard className="p-6 cursor-pointer hover:bg-white/5 transition">
            <h3 className="text-lg font-bold mb-2 flex items-center gap-2">
              <span className="material-symbols-outlined text-blue-400">
                public
              </span>
              Notify Protocol
            </h3>

            <p className="text-sm text-slate-400">
              Send an automated security notification
              to the affected DeFi protocol.
            </p>
          </GlassCard>

          <GlassCard className="p-6 cursor-pointer hover:bg-white/5 transition">
            <h3 className="text-lg font-bold mb-2 flex items-center gap-2">
              <span className="material-symbols-outlined text-green-400">
                security
              </span>
              Increase Monitoring
            </h3>

            <p className="text-sm text-slate-400">
              Escalate monitoring intensity for similar
              transaction patterns.
            </p>
          </GlassCard>

          <GlassCard className="p-6 cursor-pointer hover:bg-white/5 transition">
            <h3 className="text-lg font-bold mb-2 flex items-center gap-2">
              <span className="material-symbols-outlined text-purple-400">
                description
              </span>
              Generate Incident Report
            </h3>

            <p className="text-sm text-slate-400">
              Compile a formal incident report for
              compliance and auditing.
            </p>
          </GlassCard>

        </div>

        {/* ================= FOOTER ================= */}
        <div className="flex justify-end gap-4 mt-8">
          <SecondaryButton onClick={() => navigate("/dashboard")}>
            Return to Dashboard
          </SecondaryButton>

          <PrimaryButton onClick={() => navigate("/dashboard")}>
            Done
          </PrimaryButton>
        </div>

      </PageContainer>
    </AppLayout>
  );
}
