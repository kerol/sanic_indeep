# coding: utf-8
DATABASE = {
    'host': '127.0.0.1',
    'database': 'sanic_indeep',
    'port': 3306,
    'user': 'root',
    'password': '',
    'min_connections': 1,
    'max_connections': 10,
}

REDIS = {
    'address': ('127.0.0.1', 6379),
    'db': 0,
    'encoding': 'utf-8',
    'minsize': 1,
    'maxsize': 10,
}
