export default function SecondaryButton({ children, onClick, className = "" }) {
  return (
    <button
      onClick={onClick}
      className={`px-6 py-3 rounded-lg border border-slate-600 text-slate-300 hover:bg-slate-800 transition ${className}`}
    >
      {children}
    </button>
  );
}
