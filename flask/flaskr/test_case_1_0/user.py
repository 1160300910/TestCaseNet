from modules.Stack import Stack
from . import bp
from flask import jsonify, flash, g, redirect, render_template, request, session, url_for
from flaskr.db.Model import Peo, TestCase, query2dict, CasePath, CaseSystem
from flaskr.db_init import DB
from sqlalchemy.sql import and_


@bp.route('/', methods=['GET', 'POST'])
def hello():
    response = {
        'msg': 'hello,world!'
    }
    return jsonify(response)


@bp.route('/userLogin/', methods=['POST'], strict_slashes=False)
def userLogin():
    if request.method == 'POST':
        error = ''
        peoName = request.json.get('userName')
        peo = Peo.query.filter_by(peoName=peoName).first()
        if peo:
            msg = {'peoId': peo.peoId, 'peoType': peo.peoType}
        else:
            msg = 0
            error = "该用户名尚未注册"
            flash(error)
        response = {
            'msg': msg,
            'error': error
        }
        return jsonify(response)


@bp.route('/modifyUserInfo/', methods=['POST'], strict_slashes=False)
def modifyUserInfo():
    if request.method == 'POST':
        error = ''
        userOldName = request.json.get('userOldName')
        peo = Peo.query.filter_by(peoName=userOldName).first()
        if peo:
            # 存在这个用户，可以修改其信息
            userWork = request.json.get('userWork')
            userNewName = request.json.get('userNewName')
            peo.peoName = userNewName
            peo.peoType = int(userWork)
            DB.session.flush()
            DB.session.commit()
            msg = {'peoId': peo.peoId, 'peoType': peo.peoType, 'peoName': peo.peoName}
        else:
            msg = 0
            error = "该用户名尚未注册,不可修改"
            flash(error)
        response = {
            'msg': msg,
            'error': error
        }
        return jsonify(response)


@bp.route('/userRegister/', methods=['POST'], strict_slashes=False)
def userRegister():
    if request.method == 'POST':
        peoName = request.json.get('userName')
        peoType = request.json.get('userWork')
        print(peoName, peoType)

        msg = 0
        if not peoName:
            error = '输入名字为空'
        elif not peoType:
            error = '尚未选择身份'
        elif Peo.query.filter_by(peoName=peoName).first() is not None:
            error = '用户名：{} 已经被注册过啦！'.format(peoName)
        else:
            peo1 = Peo(peoName=peoName, peoType=int(peoType))
            DB.session.add(peo1)
            DB.session.flush()
            msg = peo1.peoId
            error = None
        if error is None:
            DB.session.commit()
        flash(error)
        response = {
            'msg': msg,
            'error': error
        }
        return jsonify(response)


@bp.route('/addTestCase/', methods=['POST'], )
def addTestCase():
    if request.method == 'POST':
        fileType = request.json.get('fileType')
        caseName = request.json.get('caseName')
        entry = request.json.get('entry')
        level = request.json.get('entry')
        conditionInfo = request.json.get('conditionInfo')
        ps = request.json.get('ps')
        state = request.json.get('state')
        system_name = request.json.get('system_name')
        tag = request.json.get('tag')
        caseType = request.json.get('caseType')
        fatherID = request.json.get('fatherID')
        peoType = request.json.get('peoType')
        actionPeo = request.json.get('actionPeo')
        changePeo = request.json.get('changePeo')

        testCase1 = TestCase(caseName=caseName, level=level, entry=entry
                             , conditionInfo=conditionInfo, executeInfo=''
                             , ps=ps, state=state, system_name=system_name, tag=tag
                             , caseType=caseType, fatherID=fatherID,
                             peoType=peoType, changePeo=changePeo, actionPeo=actionPeo
                             , actionedPeo='')

        DB.session.add(testCase1)
        DB.session.commit()


@bp.route('/saveTestCase/', methods=['POST'], strict_slashes=False)
def saveTestCase():
    msg = ''
    error = ''
    if request.method == 'POST':
        caseId = request.json.get('caseId')
        fatherId = request.json.get('fatherId')
        system_name = request.json.get('system_name')

        caseName = request.json.get('caseName')
        test_level = request.json.get('test_level')
        preCondition = request.json.get('preCondition')
        actionCondition = request.json.get('actionCondition')
        preResult = request.json.get('preResult')
        ps = request.json.get('ps')
        tag = request.json.get('tag')
        changer = request.json.get('changer')
        fileType = request.json.get('fileType')

        state = '1'
        caseType = '1'  # 未执行，无需被执行
        peoType = '1'  # 暂定为测试
        actionPeo = -1  # 暂定数据

        peo = Peo.query.filter_by(peoName=changer).first()

        if system_name:
            msg = setSystem(system_name, system_name)

        if peo is not None:
            print(peo.peoId)
            changer = peo.peoId
            actionPeo = peo.peoId
            print("==============")
        else:
            error = '没有id：{}！！'.format(changer)

        testCase1 = TestCase(caseId=caseId, fatherId=fatherId
                             , caseName=caseName, test_level=test_level
                             , preCondition=preCondition, actionCondition=actionCondition
                             , preResult=preResult, ps=ps, tag=tag
                             , changer=changer
                             , state=state, system_name=system_name, caseType=caseType
                             , peoType=peoType, actionPeo=actionPeo, fileType=fileType)

        if TestCase.query.filter_by(caseId=caseId).first() is not None:
            msg = msg + '用例{}被修改！！'.format(caseId)
            result = TestCase.query.filter_by(caseId=caseId).first()
            result.fatherId = fatherId
            result.caseName = caseName
            result.test_level = test_level
            result.preCondition = preCondition
            result.actionCondition = actionCondition
            result.preResult = preResult
            result.ps = ps
            result.tag = tag
            result.changer = changer
            result.state = state
            result.system_name = system_name
            result.caseType = caseType
            result.peoType = peoType
            result.actionPeo = actionPeo
            result.fileType = fileType
            DB.session.commit()
        else:
            msg = msg + '用例{}被创建！！'.format(caseId)
            DB.session.add(testCase1)
            DB.session.commit()
        response = {
            'msg': msg,
            'error': error
        }

        return jsonify(response)


@bp.route('/getUserTestCases/', methods=['GET'])
def getUserTestCases():
    if request.method == 'GET':
        userId = request.args.get('userId')
        # systems = request.json.get('systems')
        result = TestCase.query.filter_by(changer=userId).all()
        if (result):
            print(result)
            result = query2dict(result)
            print(result)
            pass
        else:
            print("false")
            pass

        response = {
            'msg': result,
        }
        return jsonify(response)


def checkAndCleanTestCases():
    testcases = TestCase.query.filter(TestCase.fileType == None).all()
    for testcase in testcases:
        deleteTestCaseFolderAndFile(testcase.caseId)


'''
  获取测试用例数组
'''


@bp.route('/getUserTestCaseNodesArray/', methods=['GET'])
def getUserTestCaseNodesArray():
    checkAndCleanTestCases()  # 清理测试用例集
    error = ''
    if request.method == 'GET':
        nodes = []
        userId = request.args.get('userId')
        userName = request.args.get('userName')
        peo = Peo.query.filter_by(peoName=userName, peoId=userId).first()
        if not peo:
            error = "不存在对应的用户Id和用户名！"
            msg = 0
        else:
            # 选出全部根节点
            results = TestCase.query.filter_by(fatherId=-1).all()
            print(results)
            treeStack = Stack()
            for r in results:
                fatherNode = SetNode(r)
                treeStack.push(fatherNode)
                nodes.append(fatherNode)
            while (not treeStack.is_empty()):
                father = treeStack.pop()
                print(father)
                fatherId = father['caseId']
                children = CasePath.query.filter_by(testcase_ancestor=fatherId, level=1).all()
                print(children)
                if (children):
                    for c in children:
                        child = TestCase.query.filter_by(caseId=c.testcase_caseId).first()
                        if (child):
                            childNode = SetNode(child)
                            treeStack.push(childNode)
                            print(childNode)
                            father['children'].append(childNode)
                else:
                    print(children)
                    print("没有子节点")
            msg = nodes

        response = {
            'msg': msg,
            'error': error
        }
        print(response)
        return jsonify(response)


def SetNode(node):
    tmp = {}
    # print(node.caseId)
    tmp['caseId'] = node.caseId
    tmp['label'] = node.caseName
    tmp['type'] = node.fileType
    tmp['isEditing'] = 0
    tmp['children'] = []
    if node.fileType == 'folder':
        tmp['testCase_num'] = len(CasePath.query.filter_by(testcase_ancestor=node.caseId).all())
    else:
        tmp['testCase_num'] = 0
    return tmp


@bp.route('/getFolderTableTestCases/', methods=['GET'])
def getFolderTableTestCases():
    if request.method == 'GET':
        nodes = []
        print(request.args)
        caseId = request.args.get('caseId')
        # 获取该caseId的节点的全部子节点的用例详细信息
        children = CasePath.query.filter_by(testcase_ancestor=caseId, level=1).all()
        for c in children:
            node = TestCase.query.filter_by(caseId=c.testcase_caseId).first()
            if node:
                if node.fileType == "file":
                    nodes.append(node)
                else:
                    print(node)
                    print("文件夹")
        msg = query2dict(nodes)
        for m in msg:
            changer = Peo.query.filter_by(peoId=m['changer']).first()
            m['changer'] = changer.peoName
        print(msg)
        response = {
            'msg': msg
        }
        return jsonify(response)


@bp.route("/deleteTestCase", methods=['POST'])
def deleteTestCase():
    if request.method == 'POST':
        caseId = request.json.get('caseId')
        print(caseId)
        result = TestCase.query.filter_by(caseId=caseId).all()
        print(result)
        if (result):
            msg = True
            for d in result:
                DB.session.delete(d)
            DB.session.commit()
            error = ''
            pass
        else:
            error = '不存在对应测试用例'
            msg = False
        response = {
            'error': error,
            'msg': msg
        }
        return jsonify(response)


'''
    删除caseId下对应的测试用例和文件
'''


def deleteTestCaseFolderAndFile(caseId):
    msg = '待删除caseid：{},'.format(caseId)
    error = ''
    result = TestCase.query.filter_by(caseId=caseId).first()  # 选择出需要被删除的测试用例文件夹节点
    if (result):
        if result.fileType == 'folder' and result.fatherId == -1:
            CaseSystem.query.filter_by(system_name=result.caseName).delete()
            msg += "系统标签:{}被删除, ".format(result.caseName)
        # 循环删除其全部子节点
        # 1.查询全部子节点 删除对应路径
        nodes = CasePath.query.filter_by(testcase_ancestor=caseId).order_by(CasePath.level.desc()).all()
        for node in nodes:
            msg += "路径用例 id:{}被删除, ".format(node.testcase_caseId)
            CasePath.query.filter_by(testcase_caseId=node.testcase_caseId).delete()  # 删除对应路径
            TestCase.query.filter_by(caseId=node.testcase_caseId).delete()  # 删除对应testcase
            DB.session.commit()
        TestCase.query.filter_by(caseId=caseId).delete()
    else:
        error = '不存在对应测试用例'
        msg = False
    print(msg, error)
    return msg, error


@bp.route("/deleteTestCaseFolder", methods=['POST'])
def deleteTestCaseFolder():
    if request.method == 'POST':
        caseId = request.json.get('caseId')
        msg, error = deleteTestCaseFolderAndFile(caseId)

        response = {
            'error': error,
            'msg': msg
        }
        return jsonify(response)


@bp.route("/getNewCaseId", methods=['GET'])
def getNewCaseId():
    if request.method == 'GET':
        fatherId = -1
        testCase1 = TestCase(fatherId=fatherId)

        DB.session.add(testCase1)
        DB.session.flush()

        if (testCase1.caseId):
            msg = testCase1.caseId
            error = ''
            DB.session.commit()
        else:
            msg = ''
            error = '无'

        response = {
            'error': error,
            'msg': msg
        }
        return jsonify(response)


@bp.route("/saveTestCasePath", methods=['POST'])
def saveCasePath():
    if request.method == 'POST':
        caseId = request.json.get('caseId')
        ancestorId = request.json.get('ancestorId')
        level = request.json.get('level')
        check_path = CasePath.query.filter_by(testcase_caseId=caseId, testcase_ancestor=ancestorId, level=level).first()
        if check_path:
            pass
        else:
            testcase_path = CasePath(testcase_caseId=caseId, testcase_ancestor=ancestorId, level=level)
            DB.session.add(testcase_path)
            DB.session.commit()

        msg = ''
        error = ''
        response = {
            'error': error,
            'msg': msg
        }
        return jsonify(response)


@bp.route('/changeTreeNodeData/', methods=['POST'], strict_slashes=False)
def changeTreeNodeData():
    error = ''
    if request.method == 'POST':
        caseId = request.json.get('caseId')
        caseName = request.json.get('caseName')
        fileType = request.json.get('fileType')
        changer = request.json.get('changer')
        fatherId = request.json.get('fatherId')
        print("caseId:" + str(caseId))
        changeTestCase = TestCase.query.filter_by(caseId=caseId).first()

        print(fatherId)
        msg = ''
        if fileType == 'folder' and int(fatherId) == -1:
            msg = setSystem(changeTestCase.caseName, caseName)
        if changeTestCase is not None:
            msg += '用例{}被修改！！'.format(caseId)
            changeTestCase.caseName = caseName
            changeTestCase.fileType = fileType
            changeTestCase.changer = changer
            changeTestCase.fatherId = fatherId
        else:
            DB.session.add(changeTestCase)
            error = "没有对应Id的测试用例！！！"

        DB.session.commit()
        response = {
            'msg': msg,
            'error': error,
        }

        print(response)
        return jsonify(response)


'''
    设置定义的系统，如果没有，则直接插入，
    如果重复了，不变动
'''


def setSystem(old_system_name, new_system_name):
    system = CaseSystem.query.filter_by(system_name=old_system_name).first()
    new_system_exist = CaseSystem.query.filter_by(system_name=new_system_name).first()
    if new_system_exist:  # 不能插入
        msg = '不能插入'
        pass
    else:
        if system:
            print(system)
            msg = '系统{}被修改！！'.format(new_system_name)
            system.system_name = new_system_name
        else:
            msg = '系统{}增加！！'.format(new_system_name)
            system = CaseSystem(system_name=new_system_name)
            DB.session.add(system)

    DB.session.commit()
    return msg


@bp.route("/getProjectPeos", methods=['GET'])
def getProjectPeos():
    if request.method == 'GET':
        peos = Peo.query.all()
        msg = query2dict(peos)
        response = {
            'msg': msg
        }
        return jsonify(response)


@bp.route('/getTestCaseInfoByCaseId/', methods=['GET'])
def getTestCaseInfoByCaseId():
    if request.method == 'GET':
        caseId = request.args.get('caseId')
        testcase = TestCase.query.filter_by(caseId=caseId).first()
        if testcase:
            msg = query2dict(testcase)
        else:
            msg = ''
        response = {
            'msg': msg
        }
        return jsonify(response)


@bp.route('/updateTableColumnDataByName/', methods=['POST'], strict_slashes=False)
def updateTableColumnDataByName():
    error = ''
    if request.method == 'POST':
        column_name = request.json.get('column_name')
        column_data = request.json.get('column_data')
        caseId = request.json.get('caseId')

        testcase = TestCase.query.filter_by(caseId=caseId).first()
        print(testcase)
        print(column_name)
        if testcase is not None:
            msg = '用例{}被修改！！'.format(caseId)
            if column_name == 'preCondition':
                testcase.preCondition = column_data
            elif column_name == 'caseName':
                testcase.caseName = column_data
            elif column_name == 'actionCondition':
                testcase.actionCondition = column_data
            elif column_name == 'preResult':
                testcase.preResult = column_data
            elif column_name == 'ps':
                testcase.ps = column_data
            elif column_name == 'changer':
                # todo:!统一角色id和角色名的引用
                changer = Peo.query.filter_by(peoName=column_data).first()
                testcase.changer = changer.peoId
            elif column_name == 'test_level':
                testcase.test_level = column_data
            else:
                msg = ''
                error = '查找不到用例属性'
            DB.session.commit()
        else:
            msg = ''
            error = '错误修改！不存在该 Id 的testcase'

        response = {
            'msg': msg,
            'error': error
        }
        return jsonify(response)


@bp.route('/getQAPeoData/', methods=['GET'], strict_slashes=False)
def getQAPeoData():
    error = ''
    if request.method == 'GET':
        peos = Peo.query.filter_by(peoType=1).all()
        if peos:
            msg = query2dict(peos)
        else:
            msg = ""
            error = "未找到对应人员"
        response = {
            'msg': msg,
            'error': error
        }
        return jsonify(response)


@bp.route('/getProjectSystemsData/', methods=['GET'], strict_slashes=False)
def getProjectSystemsData():
    error = ''
    if request.method == 'GET':
        testcaseFolders = TestCase.query.filter_by(fatherId=-1, fileType='folder').all()
        if testcaseFolders:
            msg = query2dict(testcaseFolders)
        else:
            msg = ""
            error = "未找到对应测试用例系统"
        response = {
            'msg': msg,
            'error': error
        }
        return jsonify(response)


@bp.route('/getSelectedTableDatas/', methods=['POST'], strict_slashes=False)
def getSelectedTableDatas():
    error = ''
    if request.method == 'POST':

        caseSystem = request.json.get('caseSystem')
        QA = request.json.get('QA')
        test_level = request.json.get('test_level')
        peo = request.json.get('peo')
        tag = request.json.get('tag')
        print("caseSystem: {} , QA: {} ,test_level : {} ,peo: {},tag:{}".format(caseSystem, QA, test_level, peo, tag))
        condition = (TestCase.caseId > 0)
        test_results = []
        if not caseSystem and not QA and not test_level and not peo and not tag:
            test_results = TestCase.query.filter_by(fileType='file').all()
            msg = query2dict(test_results)
            response = {
                'msg': msg,
                'error': error
            }
            return jsonify(response)

        if caseSystem:
            testcases = CasePath.query.filter_by(testcase_ancestor=caseSystem).all()
            if testcases:
                for t in testcases:
                    print(t.testcase_caseId)
                    condition = (TestCase.caseId == t.testcase_caseId)
                    condition = and_(condition, TestCase.fileType == 'file')
                    if QA:
                        condition = and_(condition, TestCase.changer == QA)
                    if test_level:
                        condition = and_(condition, TestCase.test_level == test_level)
                    if peo:
                        condition = and_(condition, TestCase.actionPeo == peo)
                    if tag:
                        condition = and_(condition, TestCase.tag == tag)

                    print(condition)
                    testcase = TestCase.query.filter(condition).all()
                    print(testcase)
                    for c in testcase:
                        test_results.append(c)
                msg = query2dict(test_results)
            else:
                msg = ""
                error = "对应系统:{} 下的测试用例为空".format(TestCase.query.filter_by(caseId=caseSystem).first().caseName)
        else:
            if QA:
                condition = and_(condition, TestCase.changer == QA)
            if test_level:
                condition = and_(condition, TestCase.test_level == test_level)
            if peo:
                condition = and_(condition, TestCase.actionPeo == peo)
            if tag:
                condition = and_(condition, TestCase.tag == tag)

            condition = and_(condition, TestCase.fileType == 'file')
            print(condition)
            test_results = TestCase.query.filter(condition).all()
            if test_results:
                msg = query2dict(test_results)
            else:
                msg = ""
                error = "对应测试用例为空"
        response = {
            'msg': msg,
            'error': error
        }
        return jsonify(response)


@bp.route('/uploadExcelFile/', methods=['POST'], strict_slashes=False)
def handle_upload_file():
    if request.method == "POST":
        import xlrd
        file_data = request.files.get("file")  # 获取文件要用request.FILES
        f = file_data.read()
        clinic_file = xlrd.open_workbook(file_contents=f)
        # sheet1
        table = clinic_file.sheet_by_index(2)
        # 输出每一行的内容
        # table.nrows获取该sheet中的有效行数
        deal_sheet_contains(table)

    response = {"meta": 200, "msg": "ok"}
    return jsonify(response)


'''
    处理excel的列表内容
'''


def deal_sheet_contains(table_data):
    # 构造存储列表
    tables = []
    for row_num in range(1, table_data.nrows):
        tables.append(table_data.row_values(row_num))

    print(table_data.merged_cells)
    for merge in table_data.merged_cells:
        row_s = merge[0]
        row_e = merge[1]
        column_s = merge[2]
        column_e = merge[3]
        for row in range(row_s, row_e):
            for column in range(column_s, column_e):
                tables[row - 1][column] = table_data.cell_value(row_s, column_s)

    names = table_data.row_values(0)
    max_depth = get_max_depth(names)

    for t in tables:
        print(t)
    saveTestCaseTable(tables, max_depth)


'''
    将测试用例保存到数据库
'''


def saveTestCaseTable(tables, depth):
    for t in tables:
        allNullNode = 0
        for i in range(0, depth):
            if t[i] == '':
                allNullNode += 1
        nullNode = 0
        print(t)
        fileType = 'file'
        fatherId = 1
        caseName = t[depth].strip()
        test_level = t[depth + 1].strip()
        preCondition = t[depth + 2].strip()
        actionCondition = t[depth + 3].strip()
        preResult = t[depth + 4].strip()
        ps = t[depth + 5].strip()
        tag = t[depth + 6].strip()

        testcase = TestCase(caseName=caseName, fileType=fileType, fatherId=fatherId, test_level=test_level,
                            preCondition=preCondition, actionCondition=actionCondition, preResult=preResult,
                            ps=ps, changer=1)
        DB.session.add(testcase)
        DB.session.flush()
        DB.session.commit()

        father = -1
        for path in range(0, depth):
            set_path_folders(father, t[path].strip())
            # 处理测试用例路径  testCase1
            if t[path] == '':  # 路径名需要有值
                nullNode += 1
            else:
                caseName = t[path].strip()  # 测试用例名
                if path == 0:
                    fatherId = -1
                else:
                    fatherId = 0
                fileType = 'folder'
                pathNode = TestCase.query.filter_by(caseName=caseName).first()
                if not pathNode:
                    node_case = TestCase(caseName=caseName, fileType=fileType, fatherId=fatherId)
                    DB.session.add(node_case)
                    DB.session.flush()
                    DB.session.commit()
                    testcase_ancestor = node_case.caseId
                else:
                    testcase_ancestor = pathNode.caseId

                level = (depth - allNullNode) - path + nullNode

                print("nullnODE", nullNode, "path: ", path, 'level:', level)
                testcase_caseId = testcase.caseId
                check_path = CasePath(testcase_caseId=testcase_caseId,
                                      testcase_ancestor=testcase_ancestor,
                                      level=level)
                # print(caseName,t[path])
                DB.session.add(check_path)
                DB.session.commit()
                father = t[path].strip()


def get_max_depth(names):
    max_depth = 0
    for name in names:
        if '用例Suite' in name:
            max_depth += 1
    return max_depth


def set_path_folders(father, nowNode):
    if father == -1 or nowNode == '':
        return
    if father == nowNode:
        level = 0
    else:
        level = 1

    print(father, nowNode)
    father_node = TestCase.query.filter_by(caseName=father).first()
    if father_node:
        testcase_ancestor = father_node.caseId
    else:
        father_node = TestCase(caseName=father, fileType='folder', fatherId=0)
        DB.session.add(father_node)
        DB.session.flush()
        testcase_ancestor = father_node.caseId

    now_node = TestCase.query.filter_by(caseName=nowNode).first()
    if now_node:
        testcase_caseId = now_node.caseId
    else:
        now_node = TestCase(caseName=nowNode, fileType='folder', fatherId=0)
        DB.session.add(now_node)
        DB.session.flush()
        testcase_caseId = now_node.caseId
    path = CasePath.query.filter_by(testcase_caseId=testcase_caseId, testcase_ancestor=testcase_ancestor).first()
    if path:
        print(path.pathId)
        return
    else:
        now_path = CasePath(testcase_caseId=testcase_caseId, testcase_ancestor=testcase_ancestor, level=level)
        DB.session.add(now_path)
        DB.session.commit()
