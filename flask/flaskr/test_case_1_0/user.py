from modules.Stack import Stack
from . import bp
from flask import jsonify, flash, g, redirect, render_template, request, session, url_for
from flaskr.db.Model import Peo, TestCase, query2dict, CasePath
from flaskr.db_init import DB


@bp.route('/', methods=['GET', 'POST'])
def hello():
    response = {
        'msg': 'hello,world!'
    }
    return jsonify(response)


@bp.route('/register/', methods=['GET', 'POST'], strict_slashes=False)
def register():
    if request.method == 'POST':
        print(request.get_json())
        peoName = request.json.get('name')
        peoType = request.json.get('work')
        peo1 = Peo(peoName=peoName, peoType=int(peoType))
        print(peoName, peoType)
        error = None
        if not peoName:
            error = '请输入你的名字~'
        elif not peoType:
            error = '请选择你的身份~'
        elif Peo.query.filter_by(peoName=peoName).first() is not None:
            error = '用户{}已经注册过啦！'.format(peoName)
        if error is None:
            DB.session.add(peo1)
            DB.session.commit()
            return jsonify({'msg': 'true'})
        flash(error)
    response = {
        'msg': 'hello,world!'
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
        definedType = request.json.get('definedType')
        tag = request.json.get('tag')
        caseType = request.json.get('caseType')
        fatherID = request.json.get('fatherID')
        peoType = request.json.get('peoType')
        actionPeo = request.json.get('actionPeo')
        changePeo = request.json.get('changePeo')
        testCase1 = TestCase(caseName=caseName, level=level, entry=entry
                             , conditionInfo=conditionInfo, executeInfo=''
                             , ps=ps, state=state, definedType=definedType, tag=tag
                             , caseType=caseType, fatherID=fatherID,
                             peoType=peoType, changePeo=changePeo, actionPeo=actionPeo
                             , actionedPeo='')

        DB.session.add(testCase1)
        DB.session.commit()


@bp.route('/saveTestCase/', methods=['POST'], strict_slashes=False)
def saveTestCase():
    error = ''
    if request.method == 'POST':
        caseId = request.json.get('caseId')
        fatherId = request.json.get('fatherId')

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
        definedType = '人脉'  # 暂定人脉模块
        caseType = '1'  # 未执行，无需被执行
        peoType = '1'  # 暂定为测试
        actionPeo = -1  # 暂定数据

        peo = Peo.query.filter_by(peoName=changer).first()

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
                             , state=state, definedType=definedType, caseType=caseType
                             , peoType=peoType, actionPeo=actionPeo, fileType=fileType)

        if TestCase.query.filter_by(caseId=caseId).first() is not None:
            msg = '用例{}被修改！！'.format(caseId)
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
            result.definedType = definedType
            result.caseType = caseType
            result.peoType = peoType
            result.actionPeo = actionPeo
            result.fileType = fileType
            DB.session.commit()
        else:
            msg = '用例{}被创建！！'.format(caseId)
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


@bp.route('/getUserTestCaseNodesArray/', methods=['GET'])
def getUserTestCaseNodesArray():
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
        changeTestCase = TestCase.query.filter_by(caseId=caseId).first()
        if changeTestCase is not None:
            msg = '用例{}被修改！！'.format(caseId)
            changeTestCase.caseName = caseName
            changeTestCase.fileType = fileType
            changeTestCase.changer = changer
            changeTestCase.fatherId = fatherId
            DB.session.commit()
        else:
            msg = ''
            error = "没有对应Id的测试用例！！！"
        response = {
            'msg': msg,
            'error': error
        }
        return jsonify(response)

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
            msg=''
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
                error ='查找不到用例属性'
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
            msg=""
            error="未找到对应人员"
        response = {
            'msg': msg,
            'error': error
        }
        return jsonify(response)