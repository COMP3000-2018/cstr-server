class CSTRConfig:
    pass

class ProductionConfig(CSTRConfig):
    DOMAIN = 'https://cstr.uqcloud.net'

class DevelopmentConfig(CSTRConfig):
    DOMAIN = 'http://localhost:5000'
