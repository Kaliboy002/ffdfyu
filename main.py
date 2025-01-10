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
        # Make the API request to fetch SoundCloud music
        response = requests.get(SUPER_API_URL + message)

        # Check if the response was successful (status code 200)
        if response.status_code == 200:
            data = response.json()

            # Check if "result" exists and contains an audio URL
            if "result" in data and "url" in data["result"]:
                mp3_url = data["result"]["url"]
                title = data["result"]["title"]

                # Send the MP3 audio with title
                await update.message.reply_audio(mp3_url, caption=f"Enjoy the music: {title}")
            else:
                await update.message.reply_text("Sorry, no audio found in the provided URL or the API response.")
        else:
            await update.message.reply_text(f"Failed to retrieve data from API. Status code: {response.status_code}")

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
