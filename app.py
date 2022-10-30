from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import eventlet

eventlet.monkey_patch()

app = Flask('chatApp', static_folder="static", template_folder="templates")
app.config["SECRET_KEY"] = "bruh"
socketio = SocketIO(app)

@app.route('/')
def main():
    return render_template("index.html")

@socketio.on('message')
def handleMessage(msg):
    print(f"服务器收到了:{msg}")

@socketio.event
def joinRoom(message):
    print(message)
    join_room(message['room'])

    emit("roomJoined",{
        "user": request.sid,
        "room": message['room']
    }, to=message['room'])

@socketio.event
def leaveRoom(message):
    emit('roomLeftPersonal',{'room':message['room'],'user':request.sid})
    leave_room(message['room'])
    emit('roomLeft', {'room': message['room'], 'user': request.sid}, to = message['room'])

@socketio.event
def sendMsg(message):
    emit("SendtoAll", {
        "msg":message['msg'],
        "user":request.sid,
    }, to=message['room'])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
    socketio.run(app)