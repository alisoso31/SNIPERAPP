import configparser

class ConfigManager:
    def __init__(self, file_path='config.ini'):
        self.config = configparser.ConfigParser()
        self.file_path = file_path
        if not self.config.read(self.file_path):
            raise FileNotFoundError(f"Le fichier de configuration '{self.file_path}' est introuvable.")

    def get(self, section, key, fallback=None):
        return self.config.get(section, key, fallback=fallback)
