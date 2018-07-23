# coding: utf-8
import aioredis
from sanic import Sanic

from config.settings import settings

app = Sanic()
app.config.from_object(settings)


def register_blueprints(_app):
    from music.blueprint import bp as bp_music
    _app.blueprint(bp_music)


@app.listener('before_server_start')
async def before_server_start(app, loop):
    conf = settings.REDIS
    conf['loop'] = loop
    app.redis_pool = await aioredis.create_pool(**conf)


@app.listener('after_server_stop')
async def after_server_stop(app, loop):
    app.redis_pool.close()
    await app.redis_pool.wait_closed()



if __name__ == '__main__':
    register_blueprints(app)
    app.run(host='0.0.0.0', port=8000, access_log=False)
