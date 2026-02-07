export default function GlassCard({ children, className = "" }) {
  return (
    <div
      className={`bg-[rgba(22,27,34,0.6)] backdrop-blur-xl border border-white/10 rounded-xl ${className}`}
    >
      {children}
    </div>
  );
}
