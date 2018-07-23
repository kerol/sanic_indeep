# coding: utf-8
from sanic import response
from sanic import Blueprint

from .models import Music

bp = Blueprint('music')

@bp.route('/')
async def test(request):
    data = {}
    # mysql
    musics = await Music.objects.execute(Music.select())
    mysql = [music.to_dict() for music in musics]
    data['mysql'] = mysql

    # redis
    async with request.app.redis_pool.get() as rds:
        k, v = 'foo', 'bar'
        await rds.execute('set', k, v)
        await rds.execute('expire', k, 60)
        value = await rds.execute('get', k)
        data['redis'] = value


    return response.json({'data': data})
