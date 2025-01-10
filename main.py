import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os

# Replace with your Telegram bot token
BOT_TOKEN = "8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM"

# API base URLs
PRIMARY_API_BASE_URL = "https://api.smtv.uz/pin/?url="
FALLBACK_API_BASE_URL = "https://tele-social.vercel.app/down?url="

# Start command handler
async def start(update: Update, context):
    await update.message.reply_text("Welcome! Send me a Pinterest URL, and I'll fetch the media for you.")

# Function to process Pinterest URL
async def fetch_pinterest_media(update: Update, context):
    message = update.message.text
    if "pinterest.com" not in message:
        await update.message.reply_text("Please send a valid Pinterest URL.")
        return

    await update.message.reply_text("Processing your request. Please wait...")

    # Try the primary API (smtv.uz)
    try:
        response = requests.get(PRIMARY_API_BASE_URL + message)
        data = response.json()

        if "medias" in data and len(data["medias"]) > 0:
            # Send all available media qualities to the user
            for media in data["medias"]:
                media_url = media["url"]
                quality = media["quality"]
                file_type = media["type"]

                # Send each image URL
                if file_type == "jpg":
                    await update.message.reply_photo(media_url, caption=f"Quality: {quality}")
                # You can handle other file types here if needed

        else:
            raise Exception("No media found in the primary API response.")

    except Exception as primary_error:
        # If the primary API fails, use the fallback API (Tele-Social)
        try:
            response = requests.get(FALLBACK_API_BASE_URL + message)
            data = response.json()

            if data.get("status") and "url" in data:
                media_url = data["url"]
                filename = data["filename"]

                # Send the media from the fallback API
                await update.message.reply_photo(media_url, caption=f"Media: {filename}")

            else:
                raise Exception("No media found in the fallback API response.")

        except Exception as fallback_error:
            await update.message.reply_text(
                f"An error occurred while processing your request.\n"
                f"Primary API Error: {primary_error}\n"
                f"Fallback API Error: {fallback_error}"
            )
            return

# Main function
def main():
    # Create an Application instance
    app = Application.builder().token(BOT_TOKEN).build()

    # Add command and message handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fetch_pinterest_media))

    # Start the bot
    app.run_polling()

if __name__ == "__main__":
    main()
