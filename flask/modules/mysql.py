import MySQLdb

def openMysql():
# 打开数据库连接
    db = MySQLdb.connect("localhost", "root", "xzkdbtest", "testdb", charset='utf8' )
    return db


def createTestCaseTable():
    db = openMysql()
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    # 如果数据表已经存在使用 execute() 方法删除表。
    cursor.execute("DROP TABLE IF EXISTS TestCase")
    # 创建数据表SQL语句
    # caseId, peoType, name, level, entry, conditionInfo, executeInfo, ps,
    #              changeDate, changePeo, actionPeo, actionedPeo, actionDate, definedType, tag,
    #              caseType, fatherFile, state
    sql = """CREATE TABLE TestCase (
         caseId INT PRIMARY KEY AUTO_INCREMENT,
         peoType INT NOT NULL,
         name  CHAR(50) NOT NULL,
         level INT NOT NULL,
         entry CHAR(50) NOT NULL,
         conditionInfo CHAR(50) NOT NULL,
         executeInfo CHAR(50) NOT NULL,
         ps CHAR(50) NOT NULL,
         changeDate DATETIME NOT NULL,
         changePeo INT NOT NULL,
         actionPeo INT NOT NULL,
         actionedPeo INT NOT NULL,
         actionDate DATETIME NOT NULL,
         definedType INT NOT NULL,
         tag  CHAR(20) NOT NULL,
         caseType INT NOT NULL,
         fatherFile  CHAR(50) NOT NULL,
         state INT NOT NULL
          )"""

    cursor.execute(sql)
    db.close()


if __name__=='__main__':
    createTestCaseTable()