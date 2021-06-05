from datetime import datetime
from flaskr.db_init import DB


class Peo(DB.Model):
    __tablename__ = 'peo'
    __table_args__ = {'extend_existing': True}
    peoId = DB.Column(DB.Integer, primary_key=True,
                      unique=True, autoincrement=True)
    peoName = DB.Column(DB.String(20))
    peoType = DB.Column(DB.Integer)
    createDate = DB.Column(DB.DateTime, default=datetime.now, nullable=False)
    modifiedDate = DB.Column(
        DB.DateTime, default=datetime.now, onupdate=datetime.now)
    team = DB.Column(DB.String(20))
    headImage = DB.Column(DB.String(20))
    ip = DB.Column(DB.String(20))


class DefinedType(DB.Model):
    __tablename__ = 'defined_type'
    __table_args__ = {'extend_existing': True}
    type_name = DB.Column(DB.String(20), primary_key=True, nullable=False)

class Tag(DB.Model):
    __tablename__='tag'
    __table_args__ = {'extend_existing': True}
    tag_name = DB.Column(DB.String(20), primary_key=True, nullable=False)
    definePeo = DB.Column(DB.String(20), nullable=False)


class TestCase(DB.Model):
    # 定义表名
    __tablename__ = 'testcase'

    __table_args__ = {'extend_existing': True}
    # 定义字段
    caseId = DB.Column(DB.Integer, primary_key=True, autoincrement=True,unique=True)
    caseName = DB.Column(DB.String(64))
    level = DB.Column(DB.Integer, default='P1')
    entry = DB.Column(DB.String(64))
    conditionInfo = DB.Column(DB.String(64))
    executeInfo = DB.Column(DB.String(64),default='')
    ps = DB.Column(DB.String(64))
    state = DB.Column(DB.Enum('1','2','3'),  default='1')
    changeDate = DB.Column(DB.DateTime, default=datetime.now)
    actionDate = DB.Column(DB.DateTime, default=datetime.now, onupdate=datetime.now)
    definedType = DB.Column(DB.String(64),DB.ForeignKey('defined_type.type_name'))
    tag = DB.Column(DB.String(64),DB.ForeignKey('tag.tag_name'))
    caseType = DB.Column(DB.Enum('1','2'))
    fatherID = DB.Column(DB.Integrt,nullable=False)
    peoType = DB.Column(DB.Enum('1','2','3','4') )
    changePeo = DB.Column(DB.Integer, DB.ForeignKey('peo.peoId'))
    actionPeo = DB.Column(DB.Integer, DB.ForeignKey('peo.peoId'))
    actionedPeo = DB.Column(DB.Integer, DB.ForeignKey('peo.peoId'))

    # users = DB.relationship('User', backref='role')  # 反推与role关联的多个User模型对象

if __name__ == '__main__':
    from flaskr import create_app
    app = create_app('dev')
    with app.test_request_context():
        # 删除所有表
        DB.drop_all()
        # 创建所有表
        DB.create_all()
