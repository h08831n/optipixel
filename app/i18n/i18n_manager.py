import json
from pathlib import Path
from typing import Dict, Any
from PySide6.QtCore import QObject, Signal
from app.services.settings_service import SettingsService

RTL_LANGUAGES = {"fa", "ar"}

class I18nManager(QObject):
    language_changed = Signal(str)
    _instance = None

    def __init__(self):
        super().__init__()
        self.translations: Dict[str, str] = {}
        self.current_language = "en"
        self.i18n_dir = Path(__file__).parent
        
        # Load language from settings
        settings = SettingsService().get_settings()
        saved_lang = settings.get("general", "language", "en")
        self.load_language(saved_lang)

    @classmethod
    def instance(cls) -> "I18nManager":
        if cls._instance is None:
            cls._instance = I18nManager()
        return cls._instance

    def load_language(self, lang_code: str):
        self.current_language = lang_code
        file_path = self.i18n_dir / f"{lang_code}.json"
        
        if not file_path.exists():
            file_path = self.i18n_dir / "en.json"

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.translations = json.load(f)
        except Exception as e:
            print(f"Error loading translation file {file_path}: {e}")
            self.translations = {}

    def set_language(self, lang_code: str):
        if lang_code == self.current_language and self.translations:
            return
            
        self.load_language(lang_code)
        
        # Save to settings
        settings_service = SettingsService()
        settings = settings_service.get_settings()
        settings.set("general", "language", lang_code)
        
        self.language_changed.emit(lang_code)

    def t(self, key: str, default: str = "") -> str:
        return self.translations.get(key, default or key)

    def is_rtl(self) -> bool:
        return self.current_language in RTL_LANGUAGES

# Global helper shortcut
def tr(key: str, default: str = "") -> str:
    return I18nManager.instance().t(key, default)
