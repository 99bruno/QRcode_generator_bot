import qrcode
from PIL import Image, ImageOps
from aiogram import Bot
import tempfile


async def generate_qr_code_with_logo(bot: Bot, data: str, photo_file_id: str, border_size: int = 2,
                                     border_color: str = "white") -> str:
    """
    Generate a QR code with a logo and a border around the logo

    :param bot: telegram bot
    :param data: content of the qr code
    :param photo_file_id: id of the photo file in the telegram chat
    :param border_size: size of the border around the logo (Default value = 10)
    :param border_color: color of the border around the logo (Default value = "white")

    :return: str (qr_code_path)
    """

    # Download the photo using the file ID
    file_info = await bot.get_file(photo_file_id)
    downloaded_file = await bot.download_file(file_info.file_path)

    # Save the downloaded photo to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_logo_file:
        temp_logo_file.write(downloaded_file.read())
        logo_path = temp_logo_file.name

    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,  # controls the size of the QR Code
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # high error correction to accommodate the logo
        box_size=10,  # controls how many pixels each “box” of the QR code is
        border=4,  # controls how many boxes thick the border should be
    )

    # Add data to the QR code
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR Code instance
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    # Open the logo image
    logo = Image.open(logo_path)

    # Ensure the logo has an alpha channel
    if logo.mode != 'RGBA':
        logo = logo.convert('RGBA')

    # Calculate the maximum size of the logo (25% of the QR code size)
    max_logo_size = min(img.size[0], img.size[1]) // 4

    # Calculate the size of the logo
    logo.thumbnail((max_logo_size, max_logo_size))

    # Create a new image with a border around the logo
    bordered_logo = ImageOps.expand(logo, border=border_size, fill=border_color)

    # Calculate the position to place the bordered logo at the center of the QR code
    logo_pos = ((img.size[0] - bordered_logo.size[0]) // 2, (img.size[1] - bordered_logo.size[1]) // 2)

    # Paste the bordered logo image onto the QR code
    img.paste(bordered_logo, logo_pos, bordered_logo)

    # Save the image to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_qr_file:
        img.save(temp_qr_file.name)
        qr_code_path = temp_qr_file.name

    return qr_code_path


async def generate_qr_code(data: str) -> str:
    """
    Generate a QR code

    :param data: content of the qr code

    :return: str (qr_code_path)
    """

    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,  # controls the size of the QR Code
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # high error correction
        box_size=10,  # controls how many pixels each “box” of the QR code is
        border=4,  # controls how many boxes thick the border should be
    )

    # Add data to the QR code
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR Code instance
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    # Save the image to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_qr_file:
        img.save(temp_qr_file.name)
        qr_code_path = temp_qr_file.name

    return qr_code_path
