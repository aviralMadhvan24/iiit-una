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
    <div style={{ padding: 40 }}>
      <h1>DeFi Sentinel</h1>
      <button onClick={handleLogin}>
        Login with MetaMask
      </button>
    </div>
  );
}
