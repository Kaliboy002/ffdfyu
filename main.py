from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import requests

# Telegram Bot Token
BOT_TOKEN = "7628087790:AAEzbDoI4po7MHKeNw1jg-quRxzogHCiFAo"  # Replace with your bot token

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
        print(f"[DEBUG] Received photo URL: {photo_url}")

        # Send the photo URL to the first API
        first_response = requests.get(FIRST_API_URL + photo_url)
        print(f"[DEBUG] First API Raw Response: {first_response.text}")

        first_response_json = first_response.json()
        if first_response_json.get("status") == "ACCEPTED":
            transaction_id = first_response_json.get("transaction_id")
            print(f"[DEBUG] Transaction ID: {transaction_id}")

            # Use transaction ID in the second API
            second_response = requests.get(SECOND_API_URL + transaction_id)
            print(f"[DEBUG] Second API Raw Response: {second_response.text}")

            second_response_json = second_response.json()
            final_image_url = second_response_json.get("tmp_url")

            if final_image_url:
                # Send the resulting image back to the user
                await context.bot.send_photo(chat_id=chat_id, photo=final_image_url)
                await update.message.reply_text("Here is your processed image!")
            else:
                await update.message.reply_text("Failed to retrieve the final image. Check the second API response.")
        else:
            await update.message.reply_text("Failed to process the photo. Check the first API response.")

    except Exception as e:
        print(f"[ERROR] {e}")
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
