from solders.keypair import Keypair
from solana.rpc.api import Client
from solana.rpc.commitment import Confirmed
from solders.transaction import VersionedTransaction
from solana.rpc.types import TxOpts

class SolanaWallet:
    def __init__(self, private_key_bytes, rpc_url="https://api.mainnet-beta.solana.com" ):
        self.keypair = Keypair.from_bytes(private_key_bytes)
        self.client = Client(rpc_url)
        print(f"Wallet initialisé pour l'adresse: {self.keypair.pubkey()}")

    def get_balance(self):
        resp = self.client.get_balance(self.keypair.pubkey())
        return resp.value / 1e9  # Balance en SOL

    def sign_and_send_transaction(self, versioned_tx: VersionedTransaction):
        # Signer la transaction avec notre clé privée
        signed_tx = versioned_tx.sign([self.keypair])
        
        # Envoyer la transaction au réseau
        opts = TxOpts(skip_preflight=True, preflight_commitment=Confirmed)
        result = self.client.send_raw_transaction(bytes(signed_tx), opts=opts)
        
        return result.value

    def confirm_transaction(self, signature, commitment=Confirmed):
        print(f"Confirmation de la transaction {signature}...")
        self.client.confirm_transaction(signature, commitment)
        print("Transaction confirmée avec succès!")
