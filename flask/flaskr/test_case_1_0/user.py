from . import bp
from flask import jsonify, flash, g, redirect, render_template, request, session, url_for
from flaskr.db.Model import Peo,TestCase
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

@bp.route('/addTestCase/',methods=[ 'POST'], )
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
        testCase1=TestCase(caseName=caseName,level=level,entry=entry
                           ,conditionInfo=conditionInfo,executeInfo=''
                           ,ps=ps,state=state,definedType=definedType,tag=tag
                           ,caseType=caseType,fatherID=fatherID,
                           peoType=peoType,changePeo=changePeo,actionPeo=actionPeo
                           ,actionedPeo='')

        DB.session.add(testCase1)
        DB.session.commit()