from modules.Stack import Stack
from . import bp
from flask import jsonify, flash, g, redirect, render_template, request, session, url_for
from flaskr.db.Model import Peo, TestCase, query2dict, CasePath, CaseSystem
from flaskr.db_init import DB


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


@bp.route('/getUserTestCaseNodesArray/', methods=['GET'])
def getUserTestCaseNodesArray():
    checkAndCleanTestCases()
    if request.method == 'GET':
        nodes = []
        print(request.args)
        userId = request.args.get('userId')
        # 选出全部根节点
        results = TestCase.query.filter_by(changer=userId, fatherId=-1).all()
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

        response = {
            'msg': nodes,
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
    return tmp


@bp.route('/getFolderTableTestCases/', methods=['GET'])
def getFolderTableTestCases():
    if request.method == 'GET':
        nodes = []
        print(request.args)
        caseId = request.args.get('caseId')
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
