import logging

from aiohttp import web

from src.app import init_app


def run():
    app = init_app()
    logging.basicConfig(level="DEBUG")
    web.run_app(app, port=8080, shutdown_timeout=3)


run()
