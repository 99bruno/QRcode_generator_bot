from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

generate_qr_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Generate qr code with logo 🖼")],
        [KeyboardButton(text="Generate qr code without logo 📝")],
             ],
    resize_keyboard=True,
    input_field_placeholder="Choose"
)
