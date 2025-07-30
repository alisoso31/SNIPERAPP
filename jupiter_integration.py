import requests
from solders.transaction import VersionedTransaction
from base64 import b64decode

class JupiterTrader:
    BASE_URL = "https://quote-api.jup.ag/v6"

    def __init__(self, api_key, solana_wallet ):
        self.api_key = api_key
        self.wallet = solana_wallet
        self.headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}

    def get_quote(self, input_mint, output_mint, amount_smallest_unit, slippage=1):
        url = f"{self.BASE_URL}/quote"
        params = {
            "inputMint": input_mint,
            "outputMint": output_mint,
            "amount": amount_smallest_unit,
            "slippageBps": int(slippage * 100),
        }
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def get_swap_transaction(self, quote_response):
        url = f"{self.BASE_URL}/swap"
        payload = {
            "quoteResponse": quote_response,
            "userPublicKey": str(self.wallet.keypair.pubkey()),
            "wrapAndUnwrapSol": True,
        }
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def perform_swap(self, input_mint, output_mint, amount_smallest_unit, slippage=1):
        # 1. Obtenir la meilleure route (quote)
        print("1/3 - Récupération de la route sur Jupiter...")
        quote_resp = self.get_quote(input_mint, output_mint, amount_smallest_unit, slippage)
        
        # 2. Obtenir la transaction à signer
        print("2/3 - Récupération de la transaction à signer...")
        swap_resp = self.get_swap_transaction(quote_resp)
        swap_transaction_b64 = swap_resp['swapTransaction']
        
        # 3. Décoder, signer et envoyer la transaction
        print("3/3 - Signature et envoi de la transaction...")
        raw_tx = b64decode(swap_transaction_b64)
        versioned_tx = VersionedTransaction.from_bytes(raw_tx)
        
        signature = self.wallet.sign_and_send_transaction(versioned_tx)
        
        # Confirmer la transaction
        self.wallet.confirm_transaction(signature)
        
        return signature
