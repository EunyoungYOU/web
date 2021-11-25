# flask_server.py
from flask import Flask, render_template, request, Response, jsonify
import logging
import json, os

from flask.helpers import url_for
from pywebpush import webpush, WebPushException
import requests
import time

app = Flask(__name__)

# push notification
app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'

DER_BASE64_ENCODED_PRIVATE_KEY_FILE_PATH = os.path.join(os.getcwd(),"private_key.txt")
DER_BASE64_ENCODED_PUBLIC_KEY_FILE_PATH = os.path.join(os.getcwd(),"public_key.txt")

VAPID_PRIVATE_KEY = open(DER_BASE64_ENCODED_PRIVATE_KEY_FILE_PATH, "r+").readline().strip("\n")
VAPID_PUBLIC_KEY = open(DER_BASE64_ENCODED_PUBLIC_KEY_FILE_PATH, "r+").read().strip("\n")

VAPID_CLAIMS = {
"sub": "mailto:develop@raturi.in"
}

def send_web_push(subscription_information, message_body):
    return webpush(
        subscription_info=subscription_information,
        data=message_body,
        vapid_private_key=VAPID_PRIVATE_KEY,
        vapid_claims=VAPID_CLAIMS,
    )

@app.route("/subscription/", methods=["GET", "POST"])
def subscription():
    """
        POST creates a subscription
        GET returns vapid public key which clients uses to send around push notification
    """

    if request.method == "GET":
        return Response(response=json.dumps({"public_key": VAPID_PUBLIC_KEY}),
            headers={"Access-Control-Allow-Origin": "*"}, content_type="application/json")

    subscription_token = request.get_json("subscription_token")
    return Response(status=201, mimetype="application/json")



@app.route("/push_v1/", methods=['POST'])
def push_v1():
    message = "Fire ! Run !"
    print("is_json",request.is_json)

    if not request.json or not request.json.get('sub_token'):
        return jsonify({'failed':1})

    print("request.json",request.json)

    token = request.json.get('sub_token') + '\n'

    f= open('./static/sub_token.txt', 'a+').write(token)

    try:
        token = json.loads(token)
        send_web_push(token, message)
        return jsonify({'success':1})
    except Exception as e:
        print("error",e)
        return jsonify({'failed':str(e)})
# end

@app.route('/')
@app.route('/index')
def index():
    return render_template('web_index.html')

@app.route('/fire', methods = ['GET','POST'])
def fire():
    global fire_locate
    response = requests.post('http://161.122.53.222:8080/receive')
    fire_locate = response.text #if args.video.split('::')[0].replace('./static/', '').replace('.mp4', '') == monitor: 
    print(fire_locate)

    return render_template('web_fire.html', fire_locate = fire_locate)

@app.route('/floor')
def floor():
    return render_template('web_floor.html')

@app.route('/alert', methods = ['POST'])
def alert():
    message = "Fire ! Run !"
    f= open('./static/sub_token.txt','r').readlines()

    for i in range(len(f)):
        token = f[i]
        
        token = json.loads(token)
        send_web_push(token, message)
        return jsonify({'success':1})
        #except Exception as e:
        #    print("error",e)
        #    return jsonify({'failed':str(e)})

@app.route('/b1')
def b1_f():
    user_locate = 'B1 F Section'
    
    now = time.localtime()
    data = {'loc': user_locate, 'time': "%04d/%02d/%02d %02d:%02d:%02d"%(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec), 'user_type': 'user'}
    qr_res = requests.post('http://161.122.53.222:8080/qr_receive', data = json.dumps(data))

    qr_img = './qr_img/B1_F.jpg'
    return render_template('web_B1_F.html', fire_loc = fire_locate, user_loc = user_locate, loc_img = qr_img)

@app.route('/1f')
def f1_a():
    user_locate = '1F A Section'
    
    now = time.localtime()
    data = {'loc': user_locate, 'time': "%04d/%02d/%02d %02d:%02d:%02d"%(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec), 'user_type': 'user'}
    qr_res = requests.post('http://161.122.53.222:8080/qr_receive', data = json.dumps(data))

    qr_img = './qr_img/1F_A.jpg'
    return render_template('web_1F_A.html', fire_loc = fire_locate, user_loc = user_locate, loc_img = qr_img)

@app.route('/3f')
def f3_a():
    user_locate = '3F A Section'
    
    now = time.localtime()
    data = {'loc': user_locate, 'time': "%04d/%02d/%02d %02d:%02d:%02d"%(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec), 'user_type': 'user'}
    qr_res = requests.post('http://161.122.53.222:8080/qr_receive', data = json.dumps(data))

    qr_img = './qr_img/3F_A.jpg'
    return render_template('web_3F_A.html', fire_loc = fire_locate, user_loc = user_locate, loc_img = qr_img)

if __name__ == '__main__':
    app.run(port=9080, threaded=False)