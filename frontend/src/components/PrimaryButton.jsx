export default function PrimaryButton({ children, onClick, className = "" }) {
  return (
    <button
      onClick={onClick}
      className={`px-6 py-3 rounded-lg bg-primary text-black font-bold hover:opacity-90 transition ${className}`}
    >
      {children}
    </button>
  );
}
