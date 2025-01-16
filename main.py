from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests

# Telegram Bot Token
BOT_TOKEN = "7628087790:AAEk1UPEaEWl7sshWhhDNeZI4BcwH0XyS_4"  # Replace with your actual token

# API URLs
FIRST_API_URL = "https://for-free.serv00.net/get_transaction_id.php?image="
SECOND_API_URL = "https://for-free.serv00.net/final_result_by_transaction_id.php?id="


def start(update: Update, context: CallbackContext) -> None:
    """Handles the /start command."""
    update.message.reply_text("Hello! Please send me a photo to process.")


def handle_photo(update: Update, context: CallbackContext) -> None:
    """Handles photo uploads."""
    chat_id = update.message.chat_id

    # Get the file ID of the photo
    photo_file = update.message.photo[-1]  # Get the highest resolution photo
    file_id = photo_file.file_id

    # Get the file path from Telegram
    file = context.bot.get_file(file_id)
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
            context.bot.send_photo(chat_id=chat_id, photo=final_image_url)
        else:
            update.message.reply_text("Error: Unable to fetch the processed image.")
    else:
        update.message.reply_text("Error: Unable to process the photo.")


def main() -> None:
    """Main function to run the bot."""
    updater = Updater(BOT_TOKEN)

    # Add handlers
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_photo))

    # Start the bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
