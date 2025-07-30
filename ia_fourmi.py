import time

class IAFourmi:
    def __init__(self, config, jupiter_trader, capital_alloue):
        self.config = config
        self.jupiter_trader = jupiter_trader
        self.capital_alloue = capital_alloue
        self.is_running = False
        print(f"[IAFourmi] Initialisé avec capital {self.capital_alloue}$")

    def start(self):
        print("[IAFourmi] Démarrage de l'IA Fourmi...")
        while self.is_running:
            try:
                # Exemple : acheter USDC en échange de SOL (à adapter selon stratégie)
                sol_mint = "So11111111111111111111111111111111111111112"
                usdc_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v" # USDC Mint officiel
                
                # On utilise une petite partie du capital alloué pour chaque trade
                amount_to_trade_sol = 0.01 # Exemple: trader 0.01 SOL
                amount_lamports = int(amount_to_trade_sol * 1e9)

                print(f"[IAFourmi] Tentative de swap de {amount_to_trade_sol} SOL en USDC...")
                
                resp = self.jupiter_trader.perform_swap(
                    input_mint=sol_mint,
                    output_mint=usdc_mint,
                    amount_smallest_unit=amount_lamports,
                    slippage=float(self.config.get('Trading', 'slippage') or 1)
                )
                print("[IAFourmi] Swap effectué, tx:", resp)
                
            except Exception as e:
                print(f"[IAFourmi] Erreur lors du swap: {e}")
            
            # Attendre avant le prochain cycle
            time.sleep(60)

    def stop(self):
        self.is_running = False
        print("[IAFourmi] Arrêt demandé.")
