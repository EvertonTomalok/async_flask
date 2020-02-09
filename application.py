"""
Demo Flask application to test the operation of Flask with socket.io

Aim is to create a webpage that is constantly updated with random numbers from a background python process.

30th May 2014

===================

Updated 13th April 2018

+ Upgraded code to Python 3
+ Used Python3 SocketIO implementation
+ Updated CDN Javascript and CSS sources

"""


from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
from threading import Thread, Event


__author__ = 'slynn'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app)

#random number Generator Thread
thread = Thread()
thread_stop_event = Event()

connected = 0


class RandomThread(Thread):
    def __init__(self):
        self.delay = 2
        super(RandomThread, self).__init__()

    def randomNumberGenerator(self):
        global connected
        """
        Generate a random number every 1 second and emit to a socketio instance (broadcast)
        Ideally to be run in a separate thread?
        """
        #infinite loop of magical random numbers
        clients = ["Everton", "Amanda", "Ivone"]
        while connected > 0:
            for client in clients:
                sleep(self.delay)
                socketio.emit('monitor', {'paciente': client}, namespace='/monitor')
        return

    def run(self):
        self.randomNumberGenerator()


@socketio.on('cadastro', namespace='/monitor')
def handle_message(message):
    print(message)
    print("Cadastrado")


@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')


@socketio.on('connect', namespace='/monitor')
def test_connect():
    # need visibility of the global thread object
    global thread, connected
    print('Client connected. Connected number: ', connected)

    # Start the random number generator thread only if the thread has not been started before.
    print("Starting Thread")
    connected += 1
    print("Connected number:: ", connected)
    if connected == 1:
        thread = RandomThread()
        thread.start()


@socketio.on('health', "/monitor")
def health(_id):
    print("Estoy aqui: ", _id)


@socketio.on('disconnect', "/monitor")
def test_disconnect():
    global connected
    if connected > 0:
        connected -= 1
    print('Client disconnected. Connected: ', connected)


if __name__ == '__main__':
    socketio.run(app)
