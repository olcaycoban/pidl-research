"""
Blockchain Entegrasyonu — Sepolia Testnet (D2)

Sözleşme: contracts/PIDLCertificate.sol
Python → Web3.py köprüsü

Fonksiyonlar:
    verify_task_on_chain    — Her görev tamamlandığında çağır
    mint_certificate        — 12 görev bittikten sonra NFT bas
    is_eligible             — Katılımcı sertifikaya hak kazandı mı?

Çevre değişkenleri (.env veya Streamlit secrets):
    SEPOLIA_RPC_URL   — Sepolia testnet RPC (Infura/Alchemy)
    CONTRACT_ADDRESS  — Dağıtılmış sözleşme adresi
    PRIVATE_KEY       — Oracle olarak işlem imzalayan cüzdan private key
"""

import os
import json
from typing import Optional
from src.config import get_api_key

# Minimal ABI (yalnızca kullanılan fonksiyonlar)
_CONTRACT_ABI = [
    {
        "name": "verifyTask",
        "type": "function",
        "stateMutability": "nonpayable",
        "inputs": [
            {"name": "student", "type": "address"},
            {"name": "taskId", "type": "uint8"}
        ],
        "outputs": []
    },
    {
        "name": "mintCertificate",
        "type": "function",
        "stateMutability": "nonpayable",
        "inputs": [
            {"name": "student", "type": "address"},
            {"name": "metadataURI", "type": "string"}
        ],
        "outputs": [{"name": "tokenId", "type": "uint256"}]
    },
    {
        "name": "isEligible",
        "type": "function",
        "stateMutability": "view",
        "inputs": [{"name": "student", "type": "address"}],
        "outputs": [{"name": "", "type": "bool"}]
    },
    {
        "name": "getCompletedTasks",
        "type": "function",
        "stateMutability": "view",
        "inputs": [{"name": "student", "type": "address"}],
        "outputs": [{"name": "", "type": "uint16"}]
    },
    {
        "name": "balanceOf",
        "type": "function",
        "stateMutability": "view",
        "inputs": [{"name": "owner", "type": "address"}],
        "outputs": [{"name": "", "type": "uint256"}]
    }
]


class BlockchainClient:
    """
    PIDL Blockchain istemcisi — Sepolia testnet.
    Blockchain devre dışıysa (key/URL eksik) tüm işlemler sessizce None döner.
    """

    def __init__(self):
        self._w3 = None
        self._contract = None
        self._account = None
        self._enabled = False
        self._init()

    def _init(self):
        rpc_url        = get_api_key("SEPOLIA_RPC_URL")
        contract_addr  = get_api_key("CONTRACT_ADDRESS")
        private_key    = get_api_key("PRIVATE_KEY")

        if not all([rpc_url, contract_addr, private_key]):
            return  # Blockchain devre dışı

        try:
            from web3 import Web3
            w3 = Web3(Web3.HTTPProvider(rpc_url))
            if not w3.is_connected():
                return

            self._w3       = w3
            self._account  = w3.eth.account.from_key(private_key)
            self._contract = w3.eth.contract(
                address=Web3.to_checksum_address(contract_addr),
                abi=_CONTRACT_ABI
            )
            self._enabled = True
        except Exception:
            pass

    @property
    def enabled(self) -> bool:
        return self._enabled

    def _send_tx(self, fn_call) -> Optional[str]:
        """İmzala ve gönder; tx hash döner."""
        try:
            nonce  = self._w3.eth.get_transaction_count(self._account.address)
            tx     = fn_call.build_transaction({
                "from":  self._account.address,
                "nonce": nonce,
                "gas":   200_000,
                "gasPrice": self._w3.eth.gas_price
            })
            signed = self._account.sign_transaction(tx)
            tx_hash = self._w3.eth.send_raw_transaction(signed.rawTransaction)
            return self._w3.to_hex(tx_hash)
        except Exception:
            return None

    def verify_task_on_chain(self, student_address: str, task_id: int) -> Optional[str]:
        """
        Görev tamamlama kaydını zincire yaz.

        Args:
            student_address: Katılımcının Ethereum cüzdan adresi
            task_id: 1-12 arası görev numarası

        Returns:
            İşlem hash'i (0x...) veya None (devre dışı / hata)
        """
        if not self._enabled:
            return None
        try:
            from web3 import Web3
            addr = Web3.to_checksum_address(student_address)
            fn   = self._contract.functions.verifyTask(addr, task_id)
            return self._send_tx(fn)
        except Exception:
            return None

    def mint_certificate(
        self,
        student_address: str,
        metadata_uri: str = "ipfs://QmPIDLResearch"
    ) -> Optional[str]:
        """
        12 görev tamamlandıktan sonra NFT sertifikası bas.

        Args:
            student_address: Katılımcının cüzdan adresi
            metadata_uri: IPFS veya HTTPS metadata URI

        Returns:
            İşlem hash'i veya None
        """
        if not self._enabled:
            return None
        try:
            from web3 import Web3
            addr = Web3.to_checksum_address(student_address)
            fn   = self._contract.functions.mintCertificate(addr, metadata_uri)
            return self._send_tx(fn)
        except Exception:
            return None

    def is_eligible(self, student_address: str) -> bool:
        """Katılımcı NFT'ye hak kazandı mı?"""
        if not self._enabled:
            return False
        try:
            from web3 import Web3
            addr = Web3.to_checksum_address(student_address)
            return self._contract.functions.isEligible(addr).call()
        except Exception:
            return False

    def get_completed_tasks_bitmask(self, student_address: str) -> int:
        """Tamamlanan görevlerin bitfield'ını döndür (0-4095)."""
        if not self._enabled:
            return 0
        try:
            from web3 import Web3
            addr = Web3.to_checksum_address(student_address)
            return self._contract.functions.getCompletedTasks(addr).call()
        except Exception:
            return 0


# Singleton istemci
blockchain = BlockchainClient()
