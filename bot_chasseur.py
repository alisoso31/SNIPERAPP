import time

class BotChasseur:
    def __init__(self, config, jupiter_trader, capital_alloue):
        self.config = config
        self.jupiter_trader = jupiter_trader
        self.capital_alloue = capital_alloue
        self.is_running = False
        print(f"[BotChasseur] Initialisé avec capital {self.capital_alloue}$")

    def start(self):
        print("[BotChasseur] Démarrage du bot chasseur...")
        while self.is_running:
            try:
                # Exemple : acheter SOL en échange d'USDC (à adapter selon stratégie)
                usdc_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v" # USDC Mint officiel
                sol_mint = "So11111111111111111111111111111111111111112"
                
                # On utilise une petite partie du capital alloué pour chaque trade
                amount_to_trade_usdc = 1.0 # Exemple: trader 1 USDC
                amount_smallest_unit = int(amount_to_trade_usdc * 1e6) # USDC a 6 décimales

                print(f"[BotChasseur] Tentative de swap de {amount_to_trade_usdc} USDC en SOL...")

                resp = self.jupiter_trader.perform_swap(
                    input_mint=usdc_mint,
                    output_mint=sol_mint,
                    amount_smallest_unit=amount_smallest_unit,
                    slippage=float(self.config.get('Trading', 'slippage') or 1)
                )
                print("[BotChasseur] Swap effectué, tx:", resp)

            except Exception as e:
                print(f"[BotChasseur] Erreur lors du swap: {e}")
            
            # Attendre avant le prochain cycle
            time.sleep(60)

    def stop(self):
        self.is_running = False
        print("[BotChasseur] Arrêt demandé.")
