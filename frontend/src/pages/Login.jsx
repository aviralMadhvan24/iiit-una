import { useNavigate } from "react-router-dom";

export default function Login() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex items-center justify-center bg-background-dark text-white">
      <div className="bg-[rgba(22,27,34,0.6)] backdrop-blur-xl border border-white/10 rounded-xl p-10 w-full max-w-md space-y-6">

        <h1 className="text-3xl font-bold text-center">
          Sentinel AI
        </h1>

        <input
          type="email"
          placeholder="name@protocol.com"
          className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg"
        />

        <input
          type="password"
          placeholder="••••••••"
          className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg"
        />

        <button
          onClick={() => navigate("/dashboard")}
          className="w-full bg-primary text-black font-bold py-3 rounded-lg"
        >
          Secure Login
        </button>

      </div>
    </div>
  );
}
