from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

BASE_DIR = Path(__file__).resolve().parent.parent

DIR_DB = BASE_DIR / 'src' / 'db'
PUBLIC_DIR = BASE_DIR / 'public' / 'uploads'