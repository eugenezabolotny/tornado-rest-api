from tornado import httpserver
from tornado import gen
from tornado.ioloop import IOLoop
import sqlite3 as sqlite
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello world\n')


class RoomerHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('GET: RoomerHandler\n')

    def post(self):
        self.write('POST: RoomerHandler\n')


def verifyDatabase():
    conn = sqlite.connect('rooms.db')
    c = conn.cursor()
    try:
        c.execute('SELECT * FROM rooms')
        print('Table already exists')
    except:
        print('Creating table \'rooms\'')
        c.execute('CREATE TABLE rooms (\
            id INT,\
            room INT,\
            fname TEXT,\
            lname TEXT)')
        print('Successfully created table \'rooms\'')
    conn.commit()
    conn.close()


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/?", MainHandler),
            (r"/api/v1/rooms/?", RoomerHandler),
            (r"/api/v1/rooms/[0-9][0-9][0-9]/?", RoomerHandler)
        ]
        tornado.web.Application.__init__(self, handlers)


def main():

    verifyDatabase()

    app = Application()
    app.listen(8000)
    IOLoop.instance().start()


if __name__ == '__main__':
    main()
