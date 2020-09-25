class Base:
    DEBUG = False
    ENV = 'production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://<username>:<password>@<host>:<port>/<database>'
    JWT_SECRET_KEY = "33b9b3de94a42d19f47df7021954eaa8"

class Development(Base):
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
<<<<<<< HEAD
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:19699815@localhost:3306/coffee_back'
=======
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ierrandonea:Abc77978155@localhost:3306/coffee_back'
>>>>>>> 86115f8daf61a9296b6fc8ce0302b834bf1676f1
    JWT_SECRET_KEY = "ba2c9a390a763c9ac2c1a1071652d21a" 