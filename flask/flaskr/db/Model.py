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
    # 用例编号，父用例文件夹id，类型（文件夹or用例）
    # 用例标题，用例等级,前置条件，执行条件，预期结果，备注，标签，修改人
    caseId = DB.Column(DB.Integer, primary_key=True, autoincrement=True,unique=True) # 用例编号
    caseName = DB.Column(DB.String(64)) # 用例标题
    preCondition = DB.Column(DB.String(64)) # 前置条件
    actionCondition = DB.Column(DB.String(64)) # 执行条件
    preResult = DB.Column(DB.String(64),default='') # 预期结果
    ps = DB.Column(DB.String(64)) # 备注
    test_level = DB.Column(DB.Integer, default='1') # 测试等级
    changer = DB.Column(DB.Integer, DB.ForeignKey('peo.peoId')) # 修改人

    fatherId = DB.Column(DB.Integer,nullable=False,) # 父节点
    childId = DB.Column(DB.Integer,nullable=False) # 孩子节点
    fileType = DB.Column(DB.String(10)) # 类型
    tag = DB.Column(DB.String(64),DB.ForeignKey('tag.tag_name')) #标签

    # 状态(是否被执行或者指派),修改日期,执行日期,用例类型（用例自定义的类型）
    # 测试用例类型，定义为 1.原测试用例，2.复制集合
    # 人员类型
    # 被指派的执行人，实际执行人，
    state = DB.Column(DB.Enum('1','2','3'),  default='1')
    definedType = DB.Column(DB.String(64),DB.ForeignKey('defined_type.type_name'))
    caseType = DB.Column(DB.Enum('1','2'))
    peoType = DB.Column(DB.Enum('1','2','3','4') )
    actionPeo = DB.Column(DB.Integer, DB.ForeignKey('peo.peoId'))
    actionedPeo = DB.Column(DB.Integer, DB.ForeignKey('peo.peoId'))

    changeDate = DB.Column(DB.DateTime, default=datetime.now)
    actionDate = DB.Column(DB.DateTime, default=datetime.now, onupdate=datetime.now)

    # users = DB.relationship('User', backref='role')  # 反推与role关联的多个User模型对象

if __name__ == '__main__':
    from flaskr import create_app
    app = create_app('dev')
    with app.test_request_context():
        # 删除所有表
        DB.drop_all()
        # 创建所有表
        DB.create_all()


def query2dict(model_list):
    if isinstance(model_list,list):  #如果传入的参数是一个list类型的，说明是使用的all()的方式查询的
        if isinstance(model_list[0],DB.Model):   # 这种方式是获得的整个对象  相当于 select * from table
            lst = []
            for model in model_list:
                dic = {}
                for col in model.__table__.columns:
                    dic[col.name] = getattr(model,col.name)
                lst.append(dic)
            return lst
        else:                           #这种方式获得了数据库中的个别字段  相当于select id,name from table
            lst = []
            for result in model_list:   #当以这种方式返回的时候，result中会有一个keys()的属性
                lst.append([dict(zip(result.keys, r)) for r in result])
            return lst
    else:                   #不是list,说明是用的get() 或者 first()查询的，得到的结果是一个对象
        if isinstance(model_list,DB.Model):   # 这种方式是获得的整个对象  相当于 select * from table limit=1
            dic = {}
            for col in model_list.__table__.columns:
                dic[col.name] = getattr(model_list,col.name)
            return dic
        else:    #这种方式获得了数据库中的个别字段  相当于select id,name from table limit = 1
            return dict(zip(model_list.keys(),model_list))