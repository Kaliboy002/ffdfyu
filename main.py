from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import requests

# Telegram Bot Token
BOT_TOKEN = "7628087790:AAEk1UPEaEWl7sshWhhDNeZI4BcwH0XyS_4"  # Replace with your actual token

# API URLs
FIRST_API_URL = "https://for-free.serv00.net/get_transaction_id.php?image="
SECOND_API_URL = "https://for-free.serv00.net/final_result_by_transaction_id.php?id="


async def start(update: Update, context) -> None:
    """Handles the /start command."""
    await update.message.reply_text("Send me a photo, and I'll process it for you!")


async def handle_photo(update: Update, context) -> None:
    """Handles photo uploads and processes them."""
    chat_id = update.message.chat_id

    try:
        # Get the file ID of the photo
        photo_file = update.message.photo[-1]  # Highest resolution photo
        file_id = photo_file.file_id

        # Get the file URL from Telegram
        file = await context.bot.get_file(file_id)
        photo_url = file.file_path
        print(f"Received photo URL: {photo_url}")

        # Send photo URL to the first API
        first_response = requests.get(FIRST_API_URL + photo_url).json()
        print(f"First API Response: {first_response}")

        if first_response.get("status") == "ACCEPTED":
            transaction_id = first_response.get("transaction_id")

            # Use transaction ID with the second API
            second_response = requests.get(SECOND_API_URL + transaction_id).json()
            print(f"Second API Response: {second_response}")

            final_image_url = second_response.get("tmp_url")
            if final_image_url:
                # Send the resulting image back to the user
                await context.bot.send_photo(chat_id=chat_id, photo=final_image_url)
                await update.message.reply_text("Here is your processed image!")
            else:
                await update.message.reply_text("Failed to retrieve the final image.")
        else:
            await update.message.reply_text("Failed to process the photo.")

    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("An error occurred while processing your photo.")


def main():
    """Main function to run the bot."""
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add command and message handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Start the bot
    app.run_polling()


if __name__ == "__main__":
    main()
