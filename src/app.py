from aiohttp import web

from routes import setup_routes


async def init_app():
    # Create webapp
    app = web.Application()
    app.cleanup_ctx.append(context)
    # init webapp routes
    setup_routes(app)
    return app


async def context(app):
    yield
