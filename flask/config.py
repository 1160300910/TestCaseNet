import os
import redis

class Config_db(object):
        """配置参数"""
        # 设置连接数据库的URL
        user = 'root'
        password = 'xzkdbtest'
        database = 'testdb'
        SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@127.0.0.1:3306/%s' % (user,password,database)

        SECRET_KEY = os.urandom(24)
        
        # 设置sqlalchemy自动更跟踪数据库
        SQLALCHEMY_TRACK_MODIFICATIONS = True
        # 禁止自动提交数据处理
        SQLALCHEMY_COMMIT_ON_TEARDOWN = True
        # 查询时会显示原始SQL语句
        SQLALCHEMY_ECHO = False
        '''

         # 非关系型数据库的配置
        REDIS_HOST = '127.0.0.1'
        REDIS_PORT = 6379
        '''
        '''
        # 配置session的扩展,session类型
        SESSION_TYPE = 'redis'
        # 创建redis链接,有密码设置密码
        SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
        # 是否对发送到浏览器上session的cookie值进行加密
        SESSION_USE_SIGNER = True
        PERMANENT_SESSION_LIFETIME = 60*60*24*2  # 生命周期
        SESSION_PERMANENT = False  # 如果设置为True,则关闭浏览器session就失效
        '''

class DevConfig(Config_db):
    # 开发环境配置
    # FLASK_ENV = 'development'
    DEBUG = True
    # PORT = 6026
    # TESTING = True
    # SERVER_NAME="localhost:6060"

class OnlineConfig(Config_db):
    # 发布环境
    pass


config = {
    'dev': DevConfig,
    'online': OnlineConfig,
}