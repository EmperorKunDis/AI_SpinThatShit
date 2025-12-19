"""
i18n - Internationalization Module for SpinThatShit
Supports 32 languages with automatic detection and user selection
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict

__all__ = ['I18n', 'get_i18n', 'SUPPORTED_LANGUAGES']

SUPPORTED_LANGUAGES = {
    'en': {'name': 'English', 'native': 'English'},
    'zh-CN': {'name': 'Chinese Simplified', 'native': '简体中文'},
    'es': {'name': 'Spanish', 'native': 'Español'},
    'hi': {'name': 'Hindi', 'native': 'हिन्दी'},
    'ar': {'name': 'Arabic', 'native': 'العربية'},
    'bn': {'name': 'Bengali', 'native': 'বাংলা'},
    'pt': {'name': 'Portuguese', 'native': 'Português'},
    'ru': {'name': 'Russian', 'native': 'Русский'},
    'ja': {'name': 'Japanese', 'native': '日本語'},
    'de': {'name': 'German', 'native': 'Deutsch'},
    'fr': {'name': 'French', 'native': 'Français'},
    'ko': {'name': 'Korean', 'native': '한국어'},
    'it': {'name': 'Italian', 'native': 'Italiano'},
    'tr': {'name': 'Turkish', 'native': 'Türkçe'},
    'vi': {'name': 'Vietnamese', 'native': 'Tiếng Việt'},
    'pl': {'name': 'Polish', 'native': 'Polski'},
    'uk': {'name': 'Ukrainian', 'native': 'Українська'},
    'nl': {'name': 'Dutch', 'native': 'Nederlands'},
    'th': {'name': 'Thai', 'native': 'ไทย'},
    'cs': {'name': 'Czech', 'native': 'Čeština'},
    'ro': {'name': 'Romanian', 'native': 'Română'},
    'el': {'name': 'Greek', 'native': 'Ελληνικά'},
    'hu': {'name': 'Hungarian', 'native': 'Magyar'},
    'sv': {'name': 'Swedish', 'native': 'Svenska'},
    'id': {'name': 'Indonesian', 'native': 'Bahasa Indonesia'},
    'fa': {'name': 'Persian', 'native': 'فارسی'},
    'he': {'name': 'Hebrew', 'native': 'עברית'},
    'ms': {'name': 'Malay', 'native': 'Bahasa Melayu'},
    'no': {'name': 'Norwegian', 'native': 'Norsk'},
    'sk': {'name': 'Slovak', 'native': 'Slovenčina'},
    'fi': {'name': 'Finnish', 'native': 'Suomi'},
    'da': {'name': 'Danish', 'native': 'Dansk'},
}


class I18n:
    """Internationalization handler"""

    def __init__(self, lang_code: str = 'en'):
        self.lang_code = lang_code
        self.translations: Dict[str, str] = {}
        self.fallback_translations: Dict[str, str] = {}

        # Load translations
        self._load_translations()

    def _load_translations(self):
        """Load translation files"""
        locale_dir = Path(__file__).parent / 'locales'

        # Load requested language
        lang_file = locale_dir / f'{self.lang_code}.json'
        if lang_file.exists():
            with open(lang_file, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)

        # Load English as fallback
        if self.lang_code != 'en':
            en_file = locale_dir / 'en.json'
            if en_file.exists():
                with open(en_file, 'r', encoding='utf-8') as f:
                    self.fallback_translations = json.load(f)

    def t(self, key: str, **kwargs) -> str:
        """
        Translate a key with optional formatting

        Args:
            key: Translation key (e.g., 'welcome.title')
            **kwargs: Format parameters for string formatting

        Returns:
            Translated string
        """
        # Navigate nested keys
        keys = key.split('.')
        value = self.translations

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                # Try fallback
                value = self.fallback_translations
                for fk in keys:
                    if isinstance(value, dict) and fk in value:
                        value = value[fk]
                    else:
                        return f"[{key}]"  # Key not found
                break

        if isinstance(value, str):
            # Format with parameters if provided
            if kwargs:
                try:
                    return value.format(**kwargs)
                except:
                    return value
            return value

        return f"[{key}]"

    def get_language_name(self) -> str:
        """Get current language native name"""
        return SUPPORTED_LANGUAGES.get(self.lang_code, {}).get('native', 'Unknown')


# Global instance
_i18n_instance: Optional[I18n] = None


def get_i18n(lang_code: Optional[str] = None) -> I18n:
    """
    Get or create i18n instance

    Args:
        lang_code: Language code (e.g., 'en', 'cs', 'zh-CN')

    Returns:
        I18n instance
    """
    global _i18n_instance

    if lang_code:
        _i18n_instance = I18n(lang_code)
    elif _i18n_instance is None:
        _i18n_instance = I18n('en')

    return _i18n_instance
