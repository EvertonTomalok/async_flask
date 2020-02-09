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
from datetime import datetime

from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
from threading import Thread, Event
from monitor import ElementConnected


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
elements_connected = []


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
            for element in elements_connected:
                for client in clients:
                    sleep(self.delay)
                    # socketio.emit('monitor', {'paciente': client}, namespace='/monitor')
                    element.emit_message(socketio, {'paciente': client})
        return

    def run(self):
        self.randomNumberGenerator()


def check_activity():
    global elements_connected
    print("Checking")
    new_list_activity = list()
    if len(elements_connected) == 0:
        print("Ninguem conectado. Skkiping")
        return
    for element in elements_connected:
        if (datetime.now() - element.date).seconds < 15:
            new_list_activity.append(element)
            print(f"Element {element.get_id} is active")
        else:
            print(f"Element {element.get_id} ISN'T ACTIVE ANYMORE.")

    elements_connected = new_list_activity
    return


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
    if not (any([True if element.get_id == _id else False for element in elements_connected])):
        elements_connected.append(ElementConnected(_id))
    else:
        for element in elements_connected:
            if element.get_id == _id:
                new_date = datetime.now()
                element.date = new_date
                print("New date setted -> ", new_date)

    check_activity()

    print(elements_connected)


@socketio.on('disconnect', "/monitor")
def test_disconnect():
    global connected
    if connected > 0:
        connected -= 1
    print('Client disconnected. Connected: ', connected)


if __name__ == '__main__':
    socketio.run(app)
