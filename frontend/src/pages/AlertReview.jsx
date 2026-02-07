import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import Modal from "../components/Modal";
import PrimaryButton from "../components/PrimaryButton";
import SecondaryButton from "../components/SecondaryButton";

import { getAlerts, verifyAlert } from "../lib/api";

export default function AlertReview() {
  const navigate = useNavigate();
  const [alert, setAlert] = useState(null);
  const [notes, setNotes] = useState("");

  useEffect(() => {
    async function loadAlert() {
      try {
        const res = await getAlerts({ limit: 1 });
        if (res.alerts && res.alerts.length > 0) {
          setAlert(res.alerts[0]);
        }
      } catch (err) {
        console.error("Failed to load alert for review", err);
      }
    }

    loadAlert();
  }, []);

  async function handleConfirm() {
    if (!alert) return;

    try {
      await verifyAlert(alert.id, {
        verified: true,
        false_positive: false,
        notes: notes || "Reviewed by security analyst",
      });

      navigate("/action");
    } catch (err) {
      console.error("Alert verification failed", err);
    }
  }

  return (
    <Modal>

      {/* ================= HEADER ================= */}
      <div className="px-8 pt-8 pb-4 flex items-center gap-4">
        <div className="flex items-center justify-center w-12 h-12 rounded-lg bg-yellow-500/20 text-yellow-500">
          <span className="material-symbols-outlined text-[32px]">
            warning
          </span>
        </div>

        <div>
          <h2 className="text-2xl font-bold">
            Confirm Alert Review
          </h2>
          <p className="text-slate-400 text-sm">
            Security Analyst Verification Step
          </p>
        </div>
      </div>

      {/* ================= BODY ================= */}
      <div className="px-8 py-4 space-y-6">
        <div className="bg-white/5 p-4 rounded-lg border border-white/10">
          <p className="text-slate-200">
            You are marking this alert as{" "}
            <span className="text-primary font-semibold">
              reviewed
            </span>
            . This action records your analysis in the
            immutable audit log.
          </p>
        </div>

        <div className="space-y-2">
          <label className="text-sm text-slate-300">
            Analyst Notes (Optional)
          </label>

          <textarea
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            className="w-full min-h-[120px] bg-background-dark/80 border border-slate-700 rounded-lg p-4 text-white resize-none"
            placeholder="Enter analysis notes..."
          />
        </div>
      </div>

      {/* ================= FOOTER ================= */}
      <div className="px-8 py-6 bg-white/[0.02] border-t border-white/5 flex justify-end gap-4">
        <SecondaryButton onClick={() => navigate("/forensic")}>
          Cancel
        </SecondaryButton>

        <PrimaryButton onClick={handleConfirm}>
          <span className="material-symbols-outlined mr-2">
            verified_user
          </span>
          Confirm Review
        </PrimaryButton>
      </div>

      {/* ================= META ================= */}
      <div className="px-8 pb-4 flex justify-between text-[10px] text-slate-600">
        <span>
          TX_ID: {alert?.tx_hash || "--"}
        </span>
        <span>
          Security Protocol v4.2.1
        </span>
      </div>

    </Modal>
  );
}
