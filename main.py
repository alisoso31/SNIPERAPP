from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from auto_trader import AutoTrader
from config_manager import ConfigManager
import threading

class SniperApp(App):
    def build(self):
        # --- Configuration ---
        # Assurez-vous d'avoir un fichier config.ini avec vos clés
        try:
            self.config = ConfigManager('config.ini')
            private_key_str = self.config.get('Wallet', 'private_key_bytes')
            # La clé privée doit être convertie de string hexadécimal en bytes
            private_key_bytes = bytes.fromhex(private_key_str)
            
            # Initialisation de l'AutoTrader
            self.trader = AutoTrader(private_key_bytes=private_key_bytes, config=self.config)
        except Exception as e:
            # Gérer l'erreur si config.ini est manquant ou incorrect
            layout = BoxLayout(orientation='vertical')
            error_label = Label(text=f"Erreur de configuration: {e}\nVérifiez votre fichier config.ini.")
            layout.add_widget(error_label)
            return layout

        # --- Interface Utilisateur ---
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=20)

        self.status_label = Label(text="Statut: Arrêté", font_size='24sp')
        
        start_button = Button(text="Démarrer le Trading", font_size='20sp', background_color=(0, 1, 0, 1))
        start_button.bind(on_press=self.start_trading_thread)

        stop_button = Button(text="Arrêter le Trading", font_size='20sp', background_color=(1, 0, 0, 1))
        stop_button.bind(on_press=self.stop_trading_thread)

        self.layout.add_widget(self.status_label)
        self.layout.add_widget(start_button)
        self.layout.add_widget(stop_button)

        return self.layout

    def start_trading_thread(self, instance):
        if not self.trader.is_running:
            self.status_label.text = "Statut: Démarrage en cours..."
            # Lancer le trading dans un thread séparé pour ne pas bloquer l'interface
            threading.Thread(target=self.trader.start_trading, daemon=True).start()
            # On met à jour le label un peu après pour laisser le temps au thread de démarrer
            # Dans une vraie app, on utiliserait des callbacks ou Clock.schedule_once
            self.status_label.text = "Statut: En cours"
        else:
            self.status_label.text = "Statut: Déjà en cours"

    def stop_trading_thread(self, instance):
        if self.trader.is_running:
            self.status_label.text = "Statut: Arrêt en cours..."
            self.trader.stop_trading()
            self.status_label.text = "Statut: Arrêté"
        else:
            self.status_label.text = "Statut: Déjà arrêté"

    def on_stop(self):
        # S'assurer que le trading est bien arrêté quand on ferme l'app
        if self.trader and self.trader.is_running:
            self.trader.stop_trading()

if __name__ == '__main__':
    SniperApp().run()
