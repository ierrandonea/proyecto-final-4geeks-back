class Base:
    DEBUG = False
    ENV = 'production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'

class Development(Base):
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db' 