import os

class Config:
    """Set Flask configuration vars."""

    # General Config
    TESTING = os.environ.get('TESTING', False)
    DEBUG = os.environ.get('DEBUG', False)
    SECRET_KEY = os.environ.get('SECRET_KEY', b'ymhUDKIuTerJLLjBXl3oo2yE6qDU5Drn')
    SESSION_COOKIE_NAME = os.environ.get('SESSION_COOKIE_NAME', 'my_cookie')

    # Database
    SQLALCHEMY_USERNAME = os.environ.get('SQLALCHEMY_USERNAME', 'jobsity')
    SQLALCHEMY_PASSWORD = os.environ.get('SQLALCHEMY_PASSWORD', 'jobsity')
    SQLALCHEMY_DATABASE_NAME = os.environ.get('SQLALCHEMY_DATABASE_NAME', 'jobsity')
    SQLALCHEMY_TABLE = os.environ.get('SQLALCHEMY_TABLE', 'migrations')
    SQLALCHEMY_DB_SCHEMA = os.environ.get('SQLALCHEMY_DB_SCHEMA', 'public')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI',
        f'postgresql+psycopg2://{SQLALCHEMY_USERNAME}:{SQLALCHEMY_PASSWORD}@jobsity-postgres:5401/{SQLALCHEMY_DATABASE_NAME}'
    )
