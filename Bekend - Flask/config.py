from datetime import timedelta

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/usermanagementcopy'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = False
    SESSION_COOKIE_SECURE = False  
    SESSION_COOKIE_SAMESITE = "None"  

    # JWT Konfiguracija
    SECRET_KEY = 'jhdvbauysdgvuahsbdauh78346187;'  
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Token traje 1h
    JWT_TOKEN_LOCATION = ['cookies']  # Token će se čuvati u HTTP-only cookie
    JWT_COOKIE_SECURE = False  
    JWT_COOKIE_HTTPONLY = False
    JWT_COOKIE_SAMESITE = "None"
    JWT_COOKIE_CSRF_PROTECT = False

