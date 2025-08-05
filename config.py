import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

    # Model Configurations
    OPENAI_MODEL = "gpt-4-turbo-preview"
    ANTHROPIC_MODEL = "claude-3-opus-20240229"
    LOCAL_MODEL = "mistral-7b-instruct"

    # Data Processing
    MAX_CHUNK_SIZE = 1000  # characters
    CHUNK_OVERLAP = 200  # characters

    # Cache
    CACHE_DIR = ".cache"
    USE_CACHE = True