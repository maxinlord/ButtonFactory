from aiogram import Router

def setup_message_routers() -> Router:
    from . import start, command_post, command_addchat, taps

    router = Router()
    router.include_router(start.router)
    router.include_router(command_post.router)
    router.include_router(command_addchat.router)
    router.include_router(taps.router)
    return router