from . import bp
from flask import jsonify, flash, g, redirect, render_template, request, session, url_for
from flaskr.db.Model import Peo, TestCase
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
        caseId = request.json.get('id')
        fatherID = request.json.get('fatherId')
        childId = request.json.get('childId')
        fileType = request.json.get('type')

        caseName = request.json.get('title')
        level = request.json.get('test_level')
        preCondition = request.json.get('preCondition')
        actionCondition = request.json.get('actionCondition')
        preResult = request.json.get('preResult')
        ps = request.json.get('ps')
        tag = request.json.get('tag')
        changePeo = request.json.get('changer')

        state = '1'
        definedType = '人脉'  # 暂定人脉模块
        caseType = '1'  # 未执行，无需被执行
        peoType = '1'  # 暂定为测试
        actionPeo = -1  # 暂定数据
        if (level == "P1"):
            level = 1
        elif (level == "P2"):
            level = 2
        elif (level == "P3"):
            level = 3
        elif (level == "P4"):
            level = 4
        peo = Peo.query.filter_by(peoName=changePeo).first()
        print(peo.peoId)
        if peo is not None:
            changePeo = peo.peoId
            actionPeo = peo.peoId
            print("==============")
        else:
            error = '没有id：{}！！'.format(changePeo)

        testCase1 = TestCase(caseId=caseId, fatherID=fatherID, childId=childId, fileType=fileType
                             , caseName=caseName, test_level=level
                             , preCondition=preCondition, actionCondition=actionCondition
                             , preResult=preResult, ps=ps, tag=tag
                             , changePeo=changePeo
                             , state=state, definedType=definedType, caseType=caseType
                             , peoType=peoType, actionPeo=actionPeo)

        if TestCase.query.filter_by(caseId=caseId).first() is not None:
            msg = '用例{}被修改！！'.format(caseId)
            result = TestCase.query.filter_by(caseId=caseId).first()
            result.fatherID = fatherID
            result.childId = childId
            result.fileType = fileType
            result.caseName = caseName
            result.level = level
            result.preCondition = preCondition
            result.actionCondition = actionCondition
            result.preResult = preResult
            result.ps = ps
            result.tag = tag
            result.changePeo = changePeo
            result.state = state
            result.definedType = definedType
            result.caseType = caseType
            result.peoType = peoType
            result.actionPeo = actionPeo
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


