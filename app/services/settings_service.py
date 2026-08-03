from app.config.settings import AppSettings

class SettingsService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SettingsService, cls).__new__(cls)
            cls._instance.settings = AppSettings()
        return cls._instance

    def get_settings(self) -> AppSettings:
        return self.settings
