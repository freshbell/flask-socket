from threading import Lock
from flask import Flask, render_template, session, request, copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from engineio.payload import Payload
from flask_cors import CORS
import json
import random

Payload.max_decode_packets = 101

thread = None
thread_lock = Lock()
async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
<<<<<<< HEAD
socketio = SocketIO(app, async_mode=async_mode, cors_allowed_origins='*')
=======
#socketio = SocketIO(app, async_mode=async_mode, cors_allowed_origins='*')
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()
>>>>>>> 7a37a7a61e098e27eb84bc5a57429480d5b316c5

# JSON 파일 open
with open('./server_json/Request.json', 'r', encoding='UTF-8') as f:
    STATE_REQUEST = json.load(f)
with open('./server_json/Move.json', 'r', encoding='UTF-8') as f:
    MOVE_JSON = json.load(f)

clients = {}

def make_route():
<<<<<<< HEAD
    # 맵 크기
    MAX_N = MAX_M = 30 
    direction_x = [1,0,-1,0]
    direction_y = [0,1,0,-1]

    x = random.sample(range(1, 31),1)[0]
    y = random.sample(range(1, 31),1)[0]
    BLOCKS = [str(x).zfill(4) + str(y).zfill(4)]

=======
    BLOCKS = []
    x, y = random.sample(range(1,31),1)[0], random.sample(range(1,31),1)[0]
    
>>>>>>> 7a37a7a61e098e27eb84bc5a57429480d5b316c5
    for _ in range(random.sample(range(20, 30),1)[0]):
        while True:
            direction = random.sample(range(0,3),1)[0]
            if 0 < x + direction_x[direction] <= MAX_N and 0 < y + direction_y[direction] <= MAX_M:
                x, y = x + direction_x[direction], y + direction_y[direction]
                break
        BLOCKS.append(str(x).zfill(4) + str(y).zfill(4))

    return BLOCKS

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/monitoring")
def monitor():
    return render_template('monitoring.html')

# sate, move 요청
def background_thread():
    while True:
<<<<<<< HEAD
        socketio.sleep(1)
        for sid in clients.keys():
            if not clients[sid]['AGV_NO'] == 'TEMP':
                MOVE_JSON['AGV_NO'] = clients[sid]['AGV_NO']
                MOVE_JSON['BLOCKS'] = clients[sid]['blocks']
                STATE_REQUEST['AGV_NO'] = clients[sid]['AGV_NO']

                socketio.emit('move_request',json.dumps(MOVE_JSON), room=sid)
                socketio.emit('state_request',json.dumps(STATE_REQUEST), room=sid)

# 연결
@socketio.on('connect')
def connect():
    global thread

    clients[request.sid] = {}
    clients[request.sid]['sid'] = request.sid
    clients[request.sid]['blocks'] = make_route()
    clients[request.sid]['AGV_NO'] = make_route()

    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

# 클라이언트로부터 AGV NO 수신
@socketio.on('my_agv_no')
def agv_no(data):
    clients[request.sid]['AGV_NO'] = data

# 상태 보고서 수신
@socketio.on('state_report')
def state(data):
    socketio.emit('state_view', data)

# 알람 보고서 수신
@socketio.on('alarm_report')
def alarm(data):
    socketio.emit('alarm_view', data)

# 연결 해제
@socketio.on('disconnect')
def disconnect():
    socketio.emit('disconnect_view', agv_no = request.sid)
    del clients[request.sid]

if __name__=="__main__":
    # local
    #socketio.run(app,host='0.0.0.0')

    # server
=======
        socketio.sleep(3)
        for AGV in clients.keys():
            if not AGV == 'Monitoring':
                MOVE_JSON['AGV_NO'] = AGV
                STATE_REQUEST['AGV_NO'] = AGV
                MOVE_JSON['BLOCKS'] = clients[AGV]['blocks']
                socketio.emit('move_request',json.dumps(MOVE_JSON), room=clients[AGV]['sid'])
                socketio.emit('state_request',json.dumps(STATE_REQUEST), room=clients[AGV]['sid'])

@socketio.on('hi')
def hi():
    print("hi")


monitor_sid = ''

@socketio.on('connect')
def connect():
    global thread
    global monitor_sid
    
    if 'AGV_NO' not in request.headers:
        #socketio.emit('connect_view', agv_no = request.headers['AGV_NO'])
        monitor_sid = request.sid
    else:
        clients[request.headers['AGV_NO']] = {}
        clients[request.headers['AGV_NO']]['sid'] = request.sid
        clients[request.headers['AGV_NO']]['blocks'] = make_route()

        with thread_lock:
            if thread is None:
                thread = socketio.start_background_task(background_thread)

@socketio.on('disconnect')
def disconnect():
    pass
    #socketio.emit('disconnect_view', agv_no = request.headers['AGV_NO'])

@socketio.on('state_report')
def state(data):
    global monitor_sid
    if not monitor_sid == '':
        pass
        #socketio.emit('state_view', data, room = monitor_sid)

@socketio.on('alarm_report')
def alarm(data):
    global monitor_sid
    if not monitor_sid == '':
        pass
        #socketio.emit('alarm_view', data, room = monitor_sid)
    

if __name__=="__main__":
    #socketio.run(app,host='0.0.0.0')
>>>>>>> 7a37a7a61e098e27eb84bc5a57429480d5b316c5
    socketio.run(app)