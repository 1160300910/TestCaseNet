SECRET_KEY='xslalal'

class PeoType():   # 角色类型描述
    Qa = 1  # 测试
    Designer = 2 # 策划
    Programer = 3 # 程序
    Pm = 4 # 进度管理人员

 
class CaseType():
    OriginalCase = 1 # 原qa编写的测试用例
    ActionCase = 2 # qa 指派到测试用例集的复制测试用例，只有QA可以通过修改执行用例，改原本的用例


class State():
    NoNeedAct = 1 # 未执行，无需执行
    TobeAct = 2  # 应该被执行，待执行
    Acted = 3 # 已经执行过了