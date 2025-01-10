import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Replace with your Telegram bot token
BOT_TOKEN = "8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM"

# API URL for the super-api API
SUPER_API_URL = "https://super-api.wineclo.com/soundcloud/?url="

# Start command handler
async def start(update: Update, context):
    await update.message.reply_text("Welcome! Send me a SoundCloud URL, and I'll fetch the music for you.")

# Function to process SoundCloud URL
async def fetch_soundcloud_media(update: Update, context):
    message = update.message.text
    if "soundcloud.com" not in message:
        await update.message.reply_text("Please send a valid SoundCloud URL.")
        return

    await update.message.reply_text("Processing your request. Please wait...")

    # Try the super-api API
    try:
        response = requests.get(SUPER_API_URL + message)
        data = response.json()

        if "result" in data:
            mp3_url = data["result"]["url"]
            title = data["result"]["title"]
            thumbnail = data["result"].get("thumb", None)

            # Send the media to the user
            if thumbnail:
                await update.message.reply_photo(
                    thumbnail,
                    caption=f"Here's your music: {title}",
                    reply_markup=None
                )
            else:
                await update.message.reply_text(f"Here's your music: {title}")

            await update.message.reply_audio(mp3_url, caption=f"Title: {title}")
        else:
            await update.message.reply_text("Sorry, no valid media found in the provided URL.")

    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

# Main function
def main():
    # Create an Application instance
    app = Application.builder().token(BOT_TOKEN).build()

    # Add command and message handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fetch_soundcloud_media))

    # Start the bot
    app.run_polling()

if __name__ == "__main__":
    main()
