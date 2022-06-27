import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'adizPJNDM69nkEaf63nm' #秘钥
    #以下是数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # 配置项用于设置数据发生变更之后是否发送信号给应用
    
    # 以下是异步处理模块celery的配置信息
    
    CELERY_BROKER_URL= 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'