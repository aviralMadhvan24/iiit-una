export async function connectWallet() {
  if (!window.ethereum) throw new Error("MetaMask not installed");

  const accounts = await window.ethereum.request({
    method: "eth_requestAccounts",
  });

  return accounts[0];
}

export async function signMessage(message, account) {
  return await window.ethereum.request({
    method: "personal_sign",
    params: [message, account],
  });
}
