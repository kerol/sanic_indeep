# coding: utf-8
from peewee import Model, BaseModel
from peewee_async import Manager, PooledMySQLDatabase, execute as _execute
from functools import partial
 # we instantiate a custom loop so we can pass it to our db manager

## from peewee_async docs:
# Also there’s no need to connect and re-connect before executing async queries
# with manager! It’s all automatic. But you can run Manager.connect() or
# Manager.close() when you need it.

class AsyncManager(Manager):
    """Inherit the peewee_async manager with our own object
       configuration

       database.allow_sync = False
    """

    def __init__(self, _model_class, *args, **kwargs):
        super(AsyncManager, self).__init__(*args, **kwargs)
        self._model_class = _model_class
        self.database.allow_sync = False

    def _do_fill(self, method, *args, **kwargs):
        _class_method = getattr(super(AsyncManager, self), method)
        pf = partial(_class_method, self._model_class)
        return pf(*args, **kwargs)

    def new(self, *args, **kwargs):
        return self._do_fill('create', *args, **kwargs)

    def get(self, *args, **kwargs):
        return self._do_fill('get', *args, **kwargs)

    def execute(self, query):
        return _execute(query)


def _get_meta_db_class(db):
    """creating a declarative class model for db"""
    class _BlockedMeta(BaseModel):
        def __new__(cls, name, bases, attrs):
            _instance = super(_BlockedMeta, cls).__new__(cls, name, bases, attrs)
            _instance.objects = AsyncManager(_instance, db)
            return _instance

    class _Base(Model, metaclass=_BlockedMeta):

        def to_dict(self):
            return self._data

        class Meta:
            database=db
    return _Base


def declarative_base(*args, **kwargs):
    """Returns a new Modeled Class after inheriting meta and Model classes"""
    db = PooledMySQLDatabase(*args, **kwargs)
    return _get_meta_db_class(db)


# init base model
from config.settings import settings
AsyncBaseModel = declarative_base(**settings.DATABASE)
