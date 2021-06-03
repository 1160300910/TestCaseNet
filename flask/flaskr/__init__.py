import os
from flask import Flask
from flask_cors import CORS
import redis
import logging
from logging.handlers import RotatingFileHandler
from .db_init import DB
from config import config



rootPath = 'D:\\Program\\ToolsAndProjects\\TestCase\\flask'
# 日志等级的设置
logging.basicConfig(level=logging.DEBUG)
# 创建日志记录器，每个日志路径，大小，保存日志的上限
# 这里参数是路径，最大存储内存，计数（因为默认是a模式，存满自动新增文件）
file_log_handler = RotatingFileHandler(filename=os.path.join(rootPath,'logs/log'), maxBytes=1024*1024, backupCount=10)
# 设置日志格式　　　　　日志等级　　　　　日志信息　　　日志行数　
formatter = logging.Formatter('%(levelname)s %(message)s %(lineno)d')
# 将日志记录器指定日志格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象添加日志记录器
logging.getLogger().addHandler(file_log_handler)


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config[config_name])
    '''
    app.config.update(
        TESTING=True,
        SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/',
        PORT = 5050
    )
    '''
    # app.config['TESTING'] = True
    # 操作句柄关联app
    DB.init_app(app)
    # Session(app)


    CORS(app, supports_credentials=True)

     # redis
    # global redis_store
    # redis_store = redis.StrictRedis(host=config[config_name].REDIS_HOST, port=config[config_name].REDIS_PORT)

    # 注册蓝图,第二个参数是这个模块对应的开始路径,url_prefix前缀
    from .test_case_1_0 import bp
    app.register_blueprint(bp, url_prefix='/test_case')

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
