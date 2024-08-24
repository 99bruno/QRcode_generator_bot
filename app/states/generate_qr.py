from aiogram.fsm.state import StatesGroup, State


class GenerateQr(StatesGroup):
    """
    Generate qr states
    """
    photo_file = State()
    qr_text = State()
