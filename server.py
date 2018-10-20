import socket
import urllib.parse

import _thread

from utils import log

from routes import (
    error,
    route_dict
)


class Request(object):

    def __init__(self, r):
        self.raw_data = r
        header, self.body = r.split('\r\n\r\n', 1)
        h = header.split('\r\n')
        parts = h[0].split()
        self.path = parts[1]
        self.method = parts[0]
        self.path, self.query = parsed_path(self.path)

    def form(self):
        body = urllib.parse.unquote_plus(self.body)
        log('form', self.body)
        log('form', body)
        args = body.split('&')
        f = {}
        log('args', args)
        for arg in args:
            k, v = arg.split('=')
            f[k] = v
        log('form() 字典', f)
        return f

    def headers_from_request(self):
        h = {}
        header = self.raw_data.split('\r\n\r\n', 1)[0]
        headers = header.split('\r\n')[1:]
        for c in headers:
            k, v = c.split(': ')
            h[k] = v
        return h


def parsed_path(path):
    index = path.find('?')
    if index == -1:
        return path, {}
    else:
        p = path[:index]
        query_string = path[index + 1:]
        args = query_string.split('&')
        query = {}
        for arg in args:
            k, v = arg.split('=')
            query[k] = v
        return p, query


def request_from_connection(connection):
    request = b''
    buffer_size = 1024
    while True:
        r = connection.recv(buffer_size)
        request += r
        if len(r) < buffer_size:
            request = request.decode()
            log('request\n {}'.format(request))
            return request


def response_for_request(request):
    """
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404
    """
    r = route_dict()
    response = r.get(request.path, error)
    return response(request)


def process_connection(connection):
    with connection:
        r = request_from_connection(connection)
        if len(r) > 0:
            request = Request(r)
            response = response_for_request(request)
            connection.sendall(response)
        else:
            connection.sendall(b'')
            log('接收到了一个空请求')


def run(host, port):
    """
    启动服务器
    """
    log('开始运行于', 'http://{}:{}'.format(host, port))
    with socket.socket() as s:
        s.bind((host, port))
        s.listen()
        while True:
            connection, address = s.accept()
            log('ip <{}>\n'.format(address))
            _thread.start_new_thread(process_connection, (connection,))



if __name__ == '__main__':
    config = dict(
        host='localhost',
        port=3000,
    )
    run(**config)
