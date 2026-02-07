import { loginWithMetaMask } from "../lib/auth";

export default function Login() {
  async function handleLogin() {
    try {
      await loginWithMetaMask();
      window.location.href = "/dashboard";
    } catch (err) {
      console.error(err);

      let message = "Authentication failed";

      if (Array.isArray(err?.data?.detail)) {
        message = err.data.detail.map(e => e.msg).join("\n");
      } else if (typeof err?.data?.detail === "string") {
        message = err.data.detail;
      } else if (err?.message) {
        message = err.message;
      }

      alert(message);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#0b0f10] relative overflow-hidden">
      
      {/* Background glow */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary/10 via-transparent to-purple-500/10 pointer-events-none"></div>

      {/* Login Card */}
      <div className="relative z-10 w-full max-w-md bg-[#111718]/90 backdrop-blur-xl border border-[#283639] rounded-2xl p-10 shadow-2xl">
        
        {/* Logo */}
        <div className="flex items-center justify-center mb-8">
          <div className="size-14 rounded-xl bg-gradient-to-br from-primary to-purple-600 flex items-center justify-center shadow-neon">
            <span className="material-symbols-outlined text-white text-3xl">
              shield_lock
            </span>
          </div>
        </div>

        {/* Title */}
        <h1 className="text-3xl font-bold text-white text-center mb-2 tracking-tight">
          DeFi Sentinel
        </h1>

        <p className="text-gray-400 text-center text-sm mb-10">
          Secure DeFi threat detection powered by AI
        </p>

        {/* Login Button */}
        <button
          onClick={handleLogin}
          className="w-full flex items-center justify-center gap-3 py-4 rounded-xl bg-gradient-to-r from-primary to-purple-600 text-white font-semibold text-lg shadow-neon hover:scale-[1.02] hover:shadow-[0_0_30px_rgba(139,92,246,0.6)] transition-all duration-300"
        >
          <img
            src="https://upload.wikimedia.org/wikipedia/commons/3/36/MetaMask_Fox.svg"
            alt="MetaMask"
            className="w-6 h-6"
          />
          Login with MetaMask
        </button>

        {/* Footer */}
        <p className="text-gray-500 text-xs text-center mt-8">
          By connecting, you confirm ownership of your wallet.
        </p>
      </div>
    </div>
  );
}
