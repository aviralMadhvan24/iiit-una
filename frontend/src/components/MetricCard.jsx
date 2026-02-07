export default function MetricCard({
  label,
  value,
  icon,
  accent = "text-primary",
  subtext,
}) {
  return (
    <div className="bg-surface-dark border border-[#283639] rounded-xl p-5 relative overflow-hidden">
      <span className={`material-symbols-outlined text-5xl absolute right-4 top-4 opacity-20 ${accent}`}>
        {icon}
      </span>

      <p className="text-gray-400 text-sm">{label}</p>
      <h3 className="text-3xl font-bold mt-2">{value}</h3>

      {subtext && (
        <p className={`text-sm mt-2 font-medium ${accent}`}>{subtext}</p>
      )}
    </div>
  );
}
