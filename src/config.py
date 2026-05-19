"""
Streamlit Cloud ve Local Environment için birleşik config yönetimi
"""
import os
import streamlit as st


def get_api_key(key_name: str, default: str = "") -> str:
    """
    Streamlit Cloud (st.secrets) ve local (.env) için birleşik API key okuma

    Args:
        key_name: API key ismi (örn: "OPENAI_API_KEY")
        default: Varsayılan değer

    Returns:
        API key değeri
    """
    # Önce Streamlit secrets'tan dene (Cloud için)
    try:
        if hasattr(st, 'secrets') and key_name in st.secrets:
            return st.secrets[key_name]
    except (FileNotFoundError, KeyError):
        pass

    # Sonra environment variable'dan dene (Local için)
    return os.getenv(key_name, default)


def get_config(key_name: str, default: str = "") -> str:
    """
    Genel konfigürasyon değerlerini oku

    Args:
        key_name: Config key ismi
        default: Varsayılan değer

    Returns:
        Config değeri
    """
    return get_api_key(key_name, default)


# Kolay erişim için önceden tanımlı fonksiyonlar
def get_openai_key() -> str:
    """OpenAI API key'i al"""
    return get_api_key("OPENAI_API_KEY")


def get_anthropic_key() -> str:
    """Anthropic API key'i al"""
    return get_api_key("ANTHROPIC_API_KEY")


def get_google_key() -> str:
    """Google AI API key'i al"""
    return get_api_key("GOOGLE_API_KEY", "")


def get_model_config() -> dict:
    """Model konfigürasyonunu al"""
    return {
        "default_model": get_config("DEFAULT_MODEL", "gpt-4o-mini"),
        "temperature": float(get_config("TEMPERATURE", "0.7")),
        "max_tokens": int(get_config("MAX_TOKENS", "2000"))
    }
