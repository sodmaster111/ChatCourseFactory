import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_HOST = os.getenv("BACKEND_HOST", "0.0.0.0")
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")

POSTGRES_DB = os.getenv("POSTGRES_DB", "chatcoursefactory")
POSTGRES_USER = os.getenv("POSTGRES_USER", "chatcourse")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "chatcourse_password")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
