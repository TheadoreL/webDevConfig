from flask import request, Flask
import requests

app = Flask(__name__)

@app.route('/auth', methods=['POST'])
def auth():
    print(request.form['code'])
    r = requests.get('https://api.weixin.qq.com/sns/jscode2session?appid=&secret=&js_code='+request.form['code']+'&grant_type=authorization_code')
    print(r.text)

if __name__ == '__main__':
    app.run()
