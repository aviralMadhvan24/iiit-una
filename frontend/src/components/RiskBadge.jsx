export default function RiskBadge({ score }) {
  let color =
    score >= 80
      ? "text-red-400 border-red-400/30 bg-red-400/10"
      : score >= 50
      ? "text-yellow-400 border-yellow-400/30 bg-yellow-400/10"
      : "text-green-400 border-green-400/30 bg-green-400/10";

  return (
    <span className={`px-3 py-1 rounded-full text-xs font-bold border ${color}`}>
      {score}
    </span>
  );
}
