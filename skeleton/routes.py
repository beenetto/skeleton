from concurrent.futures import ProcessPoolExecutor
from subprocess import Popen, run

import asyncio
import io
import os
import subprocess
import pathlib
import pyvips

from aiohttp import web
from PIL import Image

from skeleton.main.views import index


PROJECT_PATH = pathlib.Path(__file__).parent


async def vips_cli_handler(request):

    loop = asyncio.get_running_loop()
    process_pool_executor = ProcessPoolExecutor()

    request_data = await request.post()
    in_cmd = request_data['cmd']
    i = request_data['i']

    saved_file_name = await loop.run_in_executor(process_pool_executor, vips_cli, in_cmd, i)

    return web.Response(text='{} is done\n'.format(saved_file_name))


def vips_cli(in_cmd, i):
    input_folder = "/images/reads/"
    output_folder = "/images/writes/"

    if in_cmd == 'large_conv':
        output_file = output_folder + "large-vips-cli-converted-" + i + ".png"
        run([
            "vips",
            "jpegload",
            input_folder + "large.jpg",
            output_file,
            "--access=sequential"
        ])

    if in_cmd == 'large_resize':
        output_file = output_folder + "large-vips-cli-resized-" + i + ".jpg"
        run([
            "vips",
            "resize",
            input_folder + "large.jpg",
            output_file,
            "0.5"
        ])

    if in_cmd == 'medium_conv':
        output_file = output_folder + "medium-vips-cli-converted-" + i + ".png"
        run([
            "vips",
            "jpegload",
            input_folder + "medium.jpg",
            output_file,
            "--access=sequential"
        ])

    if in_cmd == 'medium_resize':
        output_file = output_folder + "medium-vips-cli-resized-" + i + ".jpg"
        run([
            "vips",
            "resize",
            input_folder + "medium.jpg",
            output_file,
            "0.5"
        ])

    return output_file


async def vips_handler(request):

    loop = asyncio.get_running_loop()
    process_pool_executor = ProcessPoolExecutor()

    request_data = await request.post()
    in_cmd = request_data['cmd']
    i = request_data['i']

    saved_file_name = await loop.run_in_executor(process_pool_executor, vips, in_cmd, i)

    return web.Response(text='{} is done\n'.format(saved_file_name))


def vips(in_cmd, i):

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

    return saved_file_name


async def pillow_handler(request):

    loop = asyncio.get_running_loop()
    process_pool_executor = ProcessPoolExecutor()

    request_data = await request.post()
    in_cmd = request_data['cmd']
    i = request_data['i']

    saved_file_name = await loop.run_in_executor(process_pool_executor, pillow, in_cmd, i)

    return web.Response(text='{} is done\n'.format(saved_file_name))


def pillow(in_cmd, i):

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

    return saved_file_name


def init_routes(app: web.Application) -> None:

    app.router.add_route('*', '/', index, name='index')
    app.add_routes([web.post('/vips', vips_handler)])
    app.add_routes([web.post('/vipscli', vips_cli_handler)])

    app.add_routes([web.post('/pillow', pillow_handler)])

    # added static dir
    app.router.add_static(
        '/static/',
        path=(PROJECT_PATH / 'static'),
        name='static',
    )
