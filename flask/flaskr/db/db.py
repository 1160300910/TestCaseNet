from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()

def init_db(app):
    # 创建数据库sqlalchemy工具对象
    db = SQLAlchemy(app)
    return db
