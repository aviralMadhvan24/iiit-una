import { useNavigate } from "react-router-dom";

import AppLayout from "../components/AppLayout";
import PageContainer from "../components/PageContainer";
import GlassCard from "../components/GlassCard";
import SecondaryButton from "../components/SecondaryButton";

export default function Forensic() {
  const navigate = useNavigate();

  return (
    <AppLayout
      headerProps={{
        title: "Wallet Forensics",
        showBack: true,
        backTo: "/warning",
        rightSlot: (
          <div className="flex items-center gap-3 text-xs font-mono">
            <span className="text-slate-400">Last Scanned:</span>
            <span className="text-white">2 mins ago</span>
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
            <p className="text-3xl font-mono font-bold mt-2">1,240</p>
          </GlassCard>

          <GlassCard className="p-5">
            <p className="text-xs text-slate-400 uppercase">
              Average Tx Size
            </p>
            <p className="text-3xl font-mono font-bold mt-2">$14.2k</p>
          </GlassCard>

          <GlassCard className="p-5">
            <p className="text-xs text-slate-400 uppercase">
              Historical Risk
            </p>
            <p className="text-xl font-bold text-yellow-400 mt-2">
              MODERATE (45)
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
                  Feb 24
                </td>
                <td className="p-4">
                  Dormant Activation
                </td>
                <td className="p-4 text-red-400 font-bold">
                  HIGH
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
                  Feb 23
                </td>
                <td className="p-4">
                  Mixer Interaction
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
