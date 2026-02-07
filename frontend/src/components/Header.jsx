import { useNavigate } from "react-router-dom";

export default function Header({
  title = "Sentinel AI",
  showBack = false,
  backTo = "/dashboard",
  rightSlot = null,
}) {
  const navigate = useNavigate();

  return (
    <header className="flex items-center justify-between border-b border-[#283639] px-6 py-4 bg-[#111718] sticky top-0 z-50">
      <div className="flex items-center gap-4">
        {showBack && (
          <button onClick={() => navigate(backTo)}>
            <span className="material-symbols-outlined text-slate-400 hover:text-white">
              arrow_back
            </span>
          </button>
        )}

        <span className="material-symbols-outlined text-primary text-2xl">
          shield_lock
        </span>
        <h1 className="text-xl font-bold">{title}</h1>
      </div>

      {rightSlot}
    </header>
  );
}
