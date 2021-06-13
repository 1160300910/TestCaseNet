from . import bp
from flask import jsonify, flash, g, redirect, render_template, request, session, url_for
from flaskr.db.Model import Peo, TestCase, query2dict
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
        childId = request.json.get('childId')

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
        if (test_level == "P1"):
            level = 1
        elif (test_level == "P2"):
            level = 2
        elif (test_level == "P3"):
            level = 3
        elif (test_level == "P4"):
            level = 4
        else:
            level = 0
        peo = Peo.query.filter_by(peoId=changer).first()

        if peo is not None:
            print(peo.peoId)
            changer = peo.peoId
            actionPeo = peo.peoId
            print("==============")
        else:
            error = '没有id：{}！！'.format(changer)

        testCase1 = TestCase(caseId=caseId, fatherId=fatherId, childId=childId
                             , caseName=caseName, test_level=level
                             , preCondition=preCondition, actionCondition=actionCondition
                             , preResult=preResult, ps=ps, tag=tag
                             , changer=changer
                             , state=state, definedType=definedType, caseType=caseType
                             , peoType=peoType, actionPeo=actionPeo,fileType=fileType)

        if TestCase.query.filter_by(caseId=caseId).first() is not None:
            msg = '用例{}被修改！！'.format(caseId)
            result = TestCase.query.filter_by(caseId=caseId).first()
            result.fatherId = fatherId
            result.childId = childId
            result.caseName = caseName
            result.test_level = level
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
        result = TestCase.query.filter_by(changer=userId, fatherId=-1).all()
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
