from subprocess import Popen
import os
import subprocess
import pathlib
import pyvips

from aiohttp import web
from skeleton.main.views import index

PROJECT_PATH = pathlib.Path(__file__).parent


async def cmd(request):

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

    # if in_cmd == 'tiff_conv':
    #     image = pyvips.Image.tiffload(
    #         '/images/reads/test.tiff', access='sequential')
    #     saved_file_name = '{}-{}.jpg'.format('tiff-converted', i)

    # if in_cmd == 'tiff_rotate':
    #     image = pyvips.Image.tiffload(
    #         '/images/reads/test.tiff', access='sequential')
    #     image.rot90()
    #     saved_file_name = '{}-{}.tiff'.format('tiff-rotated', i)

    if saved_file_name:
        image.write_to_file('/images/writes/{}'.format(saved_file_name))

    return web.Response(text='{} is done\n'.format(saved_file_name))


def init_routes(app: web.Application) -> None:

    app.router.add_route('*', '/', index, name='index')
    app.add_routes([web.post('/cmd', cmd)])

    # added static dir
    app.router.add_static(
        '/static/',
        path=(PROJECT_PATH / 'static'),
        name='static',
    )
