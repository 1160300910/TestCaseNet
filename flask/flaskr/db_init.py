
from flask_sqlalchemy import SQLAlchemy

# redis
redis_store = None
# 完成操作句柄的定义
DB = SQLAlchemy()
# 全局保护
# csrf = CSRFProtect()