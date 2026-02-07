import { ethers } from "ethers";
import api from "./api";

export async function loginWithMetaMask() {
  if (!window.ethereum) {
    throw new Error("MetaMask not installed");
  }

  // Connect wallet
  const provider = new ethers.BrowserProvider(window.ethereum);
  const signer = await provider.getSigner();
  const wallet = await signer.getAddress();

  // Get nonce
  const { nonce } = await api.request(`/auth/nonce/${wallet}`);

  // Sign message
  const signature = await signer.signMessage(
    `Login to DeFi Sentinel\nNonce: ${nonce}`
  );

  // Verify
  const res = await api.request("/auth/verify", {
    method: "POST",
    body: JSON.stringify({
      wallet,
      signature,
    }),
  });

  localStorage.setItem("token", res.access_token);
  localStorage.setItem("wallet", wallet);

  return res;
}
