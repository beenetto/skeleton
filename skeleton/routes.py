from subprocess import Popen
import io
import os
import subprocess
import pathlib
import pyvips

from aiohttp import web
from PIL import Image

from skeleton.main.views import index


PROJECT_PATH = pathlib.Path(__file__).parent


async def vips(request):

    request_data = await request.post()
    in_cmd = request_data['cmd']
    i = request_data['i']

    saved_file_name = ""

    if in_cmd == 'large_conv':
        image = pyvips.Image.new_from_file(
            '/images/reads/large.jpg', access='sequential')
        saved_file_name = '{}-{}.png'.format('large-converted', i)

    if in_cmd == 'large_resize':
        image = pyvips.Image.new_from_file(
            '/images/reads/large.jpg', access='sequential')
        image.resize(0.5)
        saved_file_name = '{}-{}.jpg'.format('large-resized', i)

    if in_cmd == 'medium_conv':
        image = pyvips.Image.new_from_file(
            '/images/reads/medium.jpg', access='sequential')
        saved_file_name = '{}-{}.png'.format('medium-converted', i)

    if in_cmd == 'medium_resize':
        image = pyvips.Image.new_from_file(
            '/images/reads/medium.jpg', access='sequential')
        image.resize(0.5)
        saved_file_name = '{}-{}.jpg'.format('medium-resized', i)

    if saved_file_name:
        image.write_to_file('/images/writes/{}'.format(saved_file_name))

    return web.Response(text='{} is done\n'.format(saved_file_name))


async def pillow(request):
    request_data = await request.post()
    in_cmd = request_data['cmd']
    i = request_data['i']

    saved_file_name = ""

    if in_cmd == 'large_conv':
        image = Image.open('/images/reads/large.jpg', mode='r')
        saved_file_name = '{}-{}.png'.format('large-pillow-converted', i)
        image.save('/images/writes/{}'.format(saved_file_name), 'PNG')

    if in_cmd == 'large_resize':
        image = Image.open('/images/reads/large.jpg', mode='r')
        image.resize(tuple(int(n/2)
                           for n in image.size), resample=Image.LANCZOS)
        saved_file_name = '{}-{}.jpg'.format('large-pillow-resized', i)
        image.save('/images/writes/{}'.format(saved_file_name), 'JPEG')

    if in_cmd == 'medium_conv':
        image = Image.open('/images/reads/medium.jpg', mode='r')
        saved_file_name = '{}-{}.png'.format('medium-pillow-converted', i)
        image.save('/images/writes/{}'.format(saved_file_name), 'PNG')

    if in_cmd == 'medium_resize':
        image = Image.open('/images/reads/medium.jpg', mode='r')
        image.resize(tuple(int(n/2)
                           for n in image.size), resample=Image.LANCZOS)
        saved_file_name = '{}-{}.jpg'.format('medium-pillow-resized', i)
        image.save('/images/writes/{}'.format(saved_file_name), 'JPEG')

    return web.Response(text='{} is done\n'.format(saved_file_name))


def init_routes(app: web.Application) -> None:

    app.router.add_route('*', '/', index, name='index')
    app.add_routes([web.post('/vips', vips)])
    app.add_routes([web.post('/pillow', pillow)])

    # added static dir
    app.router.add_static(
        '/static/',
        path=(PROJECT_PATH / 'static'),
        name='static',
    )
