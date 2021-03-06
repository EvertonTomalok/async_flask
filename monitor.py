from flask_socketio import SocketIO
from datetime import datetime


class ElementConnected:
    def __init__(self, _id):
        self._id = _id
        self._channel = f"/channel{self._id}"
        self._date = datetime.now()

    @property
    def get_id(self):
        return self._id

    @property
    def channel(self) -> str:
        return self._channel

    @property
    def date(self) -> datetime:
        return self._date

    @date.setter
    def date(self, new_date: datetime):
        self._date = new_date

    def emit_message(self, socket: SocketIO, data):
        socket.emit('monitor', data, namespace=self._channel)
