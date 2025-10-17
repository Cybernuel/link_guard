import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration for LinkGuard API"""

    # Flask settings
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

    # VirusTotal API
    VIRUSTOTAL_API_KEY = os.getenv('VIRUSTOTAL_API_KEY', '')

    # Rate limiting
    RATE_LIMIT_ENABLED = os.getenv('RATE_LIMIT_ENABLED', 'True').lower() == 'true'
    RATE_LIMIT_PER_MINUTE = int(os.getenv('RATE_LIMIT_PER_MINUTE', 60))

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    @staticmethod
    def validate():
        """Validate configuration"""
        warnings = []

        if not Config.VIRUSTOTAL_API_KEY:
            warnings.append("⚠️  VIRUSTOTAL_API_KEY not set - VirusTotal lookups disabled")

        if Config.DEBUG:
            warnings.append("⚠️  DEBUG mode enabled - not recommended for production")

        return warnings