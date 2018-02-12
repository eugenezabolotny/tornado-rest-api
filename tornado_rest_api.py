from tornado import httpserver
from tornado import gen
from tornado.ioloop import IOLoop
import sqlite3 as sqlite
# import json
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello world\n')


class HotelHandler(tornado.web.RequestHandler):
    def initialize(self, database):
        self.database = database

    def get(self):
        """ Method GET uses JSON in output"""
        cursor = self.database.cursor()
        res = cursor.execute('SELECT * FROM rooms')
        rooms = []
        for i in res.fetchall():
            rooms.append(dict(room=i[1], name=i[2] + ' ' + i[3]))
        self.write(tornado.escape.json_encode(rooms))

    def post(self):
        """ Method POST uses JSON
            curl -i -X POST -d
                '{"room":"512", "fname":"Sarah", "lname":"Connor"}'
                    localhost:8000/api/v1/rooms/
        """
        self.write(self.request.body)
        cursor = self.database.cursor()
        payload = tornado.escape.json_decode(self.request.body)
        res = cursor.execute('INSERT INTO rooms(room, fname, lname) VALUES ("{}","{}","{}")'.format(
            payload['room'], payload['fname'], payload['lname']
        ))
        self.database.commit()


class RoomHandler(tornado.web.RequestHandler):
    def initialize(self, database):
        self.database = database

    def get(self):
        self.write('GET: RoomHandler\n')

    def put(self):
        self.write('PUT: RoomHandler\n')

    def delete(self):
        self.write('DELETE: RoomHandler\n')
        # filters = self.request.arguments
        # self.write(filters)
        # cursor = self.database.cursor()
        # res = cursor.execute('DELETE FROM rooms WHERE room={}'.format(room_number_int))


def verifyDatabase():
    conn = sqlite.connect('rooms.db')
    c = conn.cursor()
    try:
        c.execute('SELECT * FROM rooms')
        print('Table already exists')
    except:
        print('Creating table \'rooms\'')
        c.execute('CREATE TABLE rooms (\
            id INTEGER PRIMARY KEY AUTOINCREMENT ,\
            room INTEGER,\
            fname TEXT,\
            lname TEXT)')
        print('Successfully created table \'rooms\'')
    conn.commit()
    conn.close()


class Application(tornado.web.Application):
    def __init__(self):
        conn = sqlite.connect('rooms.db')

        handlers = [
            (r"/?", MainHandler),
            (r"/api/v1/rooms/?", HotelHandler, dict(database=conn)),
            (r"/api/v1/rooms/[0-9][0-9][0-9]/?", RoomHandler)
        ]
        tornado.web.Application.__init__(self, handlers)


def main():
    verifyDatabase()

    app = Application()
    app.listen(8000)
    IOLoop.instance().start()


if __name__ == '__main__':
    main()
