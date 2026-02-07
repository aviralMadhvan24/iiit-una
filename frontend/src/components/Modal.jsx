export default function Modal({ children }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur">
      <div className="bg-[#1b2327] border border-white/10 rounded-xl w-full max-w-xl">
        {children}
      </div>
    </div>
  );
}
