import json

from utils import log


def save(data, path):
    """
    本函数把一个 dict 或者 list 写入文件
    data 是 dict 或者 list
    path 是保存文件的路径
    """
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        log('save', path, s, data)
        f.write(s)


def load(path):
    """
    本函数从一个文件中载入数据并转化为 dict 或者 list
    path 是保存文件的路径
    """
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        log('load', s)
        return json.loads(s)


class Model(object):

    @classmethod
    def db_path(cls):
        classname = cls.__name__
        path = '{}.txt'.format(classname)
        return path

    @classmethod
    def new(cls, form):
        m = cls(form)
        return m

    @classmethod
    def all(cls):
        """
        all 方法(类里面的函数叫方法)使用 load 函数得到所有的 models
        """
        path = cls.db_path()
        models = load(path)
        ms = [cls.new(m) for m in models]
        return ms

    def save(self):
        """
        用 all 方法读取文件中的所有 model 并生成一个 list
        把 self 添加进去并且保存进文件
        """
        models = self.all()
        log('models', models)
        models.append(self)
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)

    @classmethod
    def find_by(cls, **kwargs):
        us = cls.all()
        for u in us:
            for k, v in kwargs.items():
                if not hasattr(u, k) or not getattr(u, k) == v:
                    return None
            return u

    @classmethod
    def find_all(cls, **kwargs):
        result = []
        us = cls.all()
        for u in us:
            exist = True
            for k, v in kwargs.items():
                if not hasattr(u, k) or not getattr(u, k) == v:
                    exist = False
            if exist:
                result.append(u)
        return result

    def __repr__(self):
        classname = self.__class__.__name__
        properties = [
            '{}: ({})'.format(k, v) for k, v in self.__dict__.items()
        ]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)


class User(Model):

    def __init__(self, form):
        super().__init__()
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def validate_login(self):
        users = User.all()
        us = [u.__dict__ for u in users]
        for u in us:
            if u['username'] == self.username:
                return u['password'] == self.password
        return False

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2


class Message(Model):
    def __init__(self, form):
        self.message = form.get('message', '')
        self.author = form.get('author', '')
