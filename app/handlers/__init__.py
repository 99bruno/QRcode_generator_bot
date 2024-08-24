from aiogram import Router

from .generate_qr import router as generate_qr_router


def register_all_handlers():
    """
    Register all the routers in the handlers

    :return: router

    :raises: None
    """

    router = Router()

    router.include_router(generate_qr_router)

    return router
