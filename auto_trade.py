import threading
from ia_fourmi import IAFourmi
from bot_chasseur import BotChasseur
from jupiter_integration import JupiterTrader
from solana_wallet import SolanaWallet

class AutoTrader:
    def __init__(self, private_key_bytes, config):
        self.config = config
        self.is_running = False

        # Création du portefeuille et du trader Jupiter
        self.wallet = SolanaWallet(private_key_bytes)
        self.jupiter_trader = JupiterTrader(config.get('API', 'jupiter_api_key'), self.wallet)

        # Répartition du capital
        total_capital = float(config.get('Trading', 'trade_amount_usd') or 100.0)
        self.capital_fourmi = total_capital * 0.8
        self.capital_chasseur = total_capital * 0.2

        # Initialisation des bots avec les bons objets
        self.ia_fourmi = IAFourmi(config, self.jupiter_trader, self.capital_fourmi)
        self.bot_chasseur = BotChasseur(config, self.jupiter_trader, self.capital_chasseur)

        self.fourmi_thread = None
        self.chasseur_thread = None

    def start_trading(self):
        if not self.is_running:
            self.is_running = True
            print(">>> Démarrage du trading global <<<")
            
            self.ia_fourmi.is_running = True
            self.fourmi_thread = threading.Thread(target=self.ia_fourmi.start, daemon=True)
            self.fourmi_thread.start()
            
            self.bot_chasseur.is_running = True
            self.chasseur_thread = threading.Thread(target=self.bot_chasseur.start, daemon=True)
            self.chasseur_thread.start()

    def stop_trading(self):
        if self.is_running:
            print(">>> Arrêt du trading global demandé <<<")
            self.ia_fourmi.stop()
            self.bot_chasseur.stop()
            self.is_running = False
