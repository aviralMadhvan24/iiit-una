export default function AlertItem({
  wallet,
  amount,
  score,
  subtitle,
  onClick,
}) {
  return (
    <div
      onClick={onClick}
      className="bg-[#111718] p-3 rounded-lg border border-l-4 border-[#283639] hover:bg-[#1c2628] cursor-pointer transition"
    >
      <div className="flex justify-between mb-1">
        <span className="font-mono text-primary">{wallet}</span>
        <span className="font-bold">{amount}</span>
      </div>

      <div className="flex justify-between text-xs text-gray-400">
        <span>{subtitle}</span>
        <span className="font-bold">{score}</span>
      </div>
    </div>
  );
}
