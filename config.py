import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'temp_uploads')
CONVERTED_FOLDER = os.path.join(BASE_DIR, 'converted_files')


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500MB限制
    UPLOAD_FOLDER = UPLOAD_FOLDER
    CONVERTED_FOLDER = CONVERTED_FOLDER
    ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'flac', 'm4a', 'aac'}