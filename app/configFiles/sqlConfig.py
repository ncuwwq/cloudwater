from .Config import CONFIG


class SQLCONFIG(CONFIG):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://ncuwwq:d617e8dbb14ea79e@' + \
                              CONFIG.host + ':3306/cloudwater?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SENTRY_ENABLE = True
