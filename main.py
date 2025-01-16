from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    filters,
)
import requests

# Telegram Bot Token
BOT_TOKEN = "7628087790:AAEk1UPEaEWl7sshWhhDNeZI4BcwH0XyS_4"  # Replace with your actual token

# API URLs
FIRST_API_URL = "https://for-free.serv00.net/get_transaction_id.php?image="
SECOND_API_URL = "https://for-free.serv00.net/final_result_by_transaction_id.php?id="


async def start(update: Update, context: CallbackContext) -> None:
    """Handles the /start command."""
    await update.message.reply_text("Hello! Please send me a photo to process.")


async def handle_photo(update: Update, context: CallbackContext) -> None:
    """Handles photo uploads."""
    chat_id = update.message.chat_id

    # Get the file ID of the photo
    photo_file = update.message.photo[-1]  # Get the highest resolution photo
    file_id = photo_file.file_id

    # Get the file path from Telegram
    file = await context.bot.get_file(file_id)
    photo_url = file.file_path

    # Send photo to the first API
    first_api_response = requests.get(FIRST_API_URL + photo_url).json()

    if first_api_response.get("status") == "ACCEPTED":
        transaction_id = first_api_response.get("transaction_id")

        # Use transaction ID in the second API
        second_api_response = requests.get(SECOND_API_URL + transaction_id).json()
        final_image_url = second_api_response.get("tmp_url")

        if final_image_url:
            # Send the processed image back to the user
            await context.bot.send_photo(chat_id=chat_id, photo=final_image_url)
        else:
            await update.message.reply_text(
                "Error: Unable to fetch the processed image."
            )
    else:
        await update.message.reply_text("Error: Unable to process the photo.")


def main() -> None:
    """Main function to run the bot."""
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Run the bot
    app.run_polling()


if __name__ == "__main__":
    main()
