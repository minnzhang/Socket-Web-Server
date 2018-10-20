from utils import log
from models import User, Message


def template(name):
    """
    根据名字读取 templates 文件夹里的一个文件并返回
    """
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def route_index(request):
    """
    主页的处理函数, 返回主页的响应
    """
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    body = template('index.html')
    r = header + '\r\n' + body
    return r.encode()


def route_login(request):
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_login():
            result = '登录成功'
        else:
            result = '用户名或者密码错误'
    else:
        result = ''
    body = template('login.html')
    body = body.replace('{{result}}', result)
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    r = header + '\r\n' + body
    return r.encode()


def route_register(request):
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_register():
            u.save()
            result = '注册成功<br> <pre>{}</pre>'.format(User.all())
        else:
            result = '用户名或者密码长度必须大于2'
    else:
        result = ''
    body = template('register.html')
    body = body.replace('{{result}}', result)
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    r = header + '\r\n' + body
    return r.encode()


def route_message(request):
    """
    主页的处理函数, 返回主页的响应
    """
    log('本次请求的 method', request.method)
    if request.method == 'POST':
        data = request.form()
    elif request.method == 'GET':
        data = request.query
    else:
        raise ValueError('Unknown method')

    if 'message' in data:
        log('post', data)
        # 应该在这里保存 message_list
        m = Message.new(data)
        m.save()
        # message_list.append(data)

    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = template('message.html')
    ms = '<br>'.join([str(m) for m in Message.all()])
    body = body.replace('{{messages}}', ms)
    r = header + '\r\n' + body
    return r.encode()


def route_static(request):
    """
    静态资源的处理函数, 读取图片并生成响应返回
    """
    filename = request.query['file']
    path = 'static/{}'.format(filename)
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
        r = header + b'\r\n' + f.read()
        return r


def error(request):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    r = b'HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/html\r\n\r\n<h1>NOT FOUND</h1>'
    return r


def route_dict():
    # 路由字典
    # key 是路由(路由就是 path)
    # value 是路由处理函数(就是响应)
    r = {

        '/'        : route_index,
        '/static'  : route_static,
        '/login'   : route_login,
        '/register': route_register,
        '/messages': route_message,
    }

    return r
