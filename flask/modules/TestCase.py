from MySQLdb import cursors
from . import Peo
from globals import PeoType
from . import mysql


class TestCase():

    def __init__(self, caseId, peoType, name, level, entry, conditionInfo, executeInfo, ps,
                 changeDate, changePeo, actionPeo, actionedPeo, actionDate, definedType, tag,
                 caseType, fatherFile, state):
        self.caseId = caseId  # 用例编号，全局唯一
        self.name = name  # 测试用例名
        self.level = level  # 用例等级
        self.entry = entry  # 用例入口
        self.conditionInfo = conditionInfo  # 用例执行条件
        self.executeInfo = executeInfo  # 用例执行方法
        self.ps = ps  # 用例执行备注

        self.state = state  # 当前被执行状态
        self.changeDate = changeDate  # 用例修改日期
        self.actionDate = actionDate  # 用例执行日期
        self.definedType = definedType  # 用例自定义的类型
        self.tag = tag  # 用例自定义tag
        self.caseType = caseType  # 测试用例类型，定义为 1.原测试用例，2.复制集合

        self.fatherFile = fatherFile  # 所属父文件夹

        self.peoType = peoType  # 人员角色类型
        self.changePeo = changePeo  # 用例修改人
        self.actionPeo = actionPeo  # 用例被指派的执行人
        self.actionedPeo = actionedPeo  # 用例实际执行人

    def checkTestCase(peo: Peo):
        '''
            检查是否能创建测试用例
        '''
        if peo.peoType == PeoType.Qa:
            return True
        else:
            return False

    def saveTestCase(peo: Peo, caseId, name, level, entry, conditionInfo, executeInfo, ps,
                     changeDate, changePeo, actionPeo, actionedPeo, actionDate, definedType, tag,
                     caseType, fatherFile, state):
        '''
            保存创建的测试用例
        '''
        if not TestCase.checkTestCase(peo):
            return
        # 写数据库，id自增，nameXXX等等
        cursor = mysql.openMysql()
        sql = "INSERT INTO TestCase(caseId, peoType,name,level,entry,conditionInfo,\
                executeInfo,ps,changeDate,changePeo, actionPeo, actionedPeo, actionDate,\
                definedType,tag,caseType,fatherFile,state) \
                VALUES (%s, %s, %s, %s, %s ,%s, \
                    %s, %s, %s, %s ,%s, %s, %s,\
                 %s, %s ,%s, %s, %s )" % \
                (caseId, peo.peoType,name,level,entry,conditionInfo,\
                executeInfo,ps,changeDate,changePeo, actionPeo, actionedPeo, actionDate,\
                definedType,tag,caseType,fatherFile,state)
        cursor.execute(sql)
