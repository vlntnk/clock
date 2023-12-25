from flask import Flask, render_template
from urllib.request import urlopen
import json
from flask_socketio import SocketIO
import datetime

app = Flask(__name__)
app.secret_key = 'secret_key'
url = 'https://ipinfo.io/json'
socketio = SocketIO(app, cors_allowed_origins='*')


@app.get('/')
def index():
    info = urlopen(url)
    location = json.load(info)['city'].upper()
    return render_template('index.html', location=location)


@socketio.on('time')
def display_time():
    while True:
        time_data = {
            'hours': datetime.datetime.now().hour,
            'minutes': datetime.datetime.now().minute,
            'seconds': datetime.datetime.now().second
        }
        socketio.emit('time', time_data)
        socketio.sleep(1)


if __name__ == '__main__':
    socketio.run(app, host='localhost', debug=True, allow_unsafe_werkzeug=True)
