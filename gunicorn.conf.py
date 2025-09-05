"""
Copyright 2025 Rajul Jha <rajuljha49@gmail.com>
"""
import os

from dotenv import load_dotenv

load_dotenv()

bind = f"{os.getenv('HOST', '0.0.0.0')}:{os.getenv('PORT', '8000')}"

workers = int(os.getenv("MAX_GUNICORN_WORKERS", "1"))
