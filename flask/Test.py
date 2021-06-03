from flask import Flask
from flask import jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route('/test_case/',methods = ['GET','POST'])
def hello():
    response = {
        'msg':'hello,world!'
    }
    return jsonify(response)

# 启动运行
if __name__ == '__main__':
    app.run()   # 这样子会直接运行在本地服务器，也即是 localhost:5000