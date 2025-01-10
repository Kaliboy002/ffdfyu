import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Replace with your Telegram bot token
BOT_TOKEN = "8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM"

# API base URL for TikTok downloader
API_BASE_URL = "https://super-api.wineclo.com/tiktok/?url="

# Start command handler
async def start(update: Update, context):
    await update.message.reply_text("Welcome! Send me a TikTok URL, and I'll fetch the video for you.")

# Function to process TikTok URL
async def fetch_tiktok_media(update: Update, context):
    message = update.message.text
    if "tiktok.com" not in message:
        await update.message.reply_text("Please send a valid TikTok URL.")
        return

    await update.message.reply_text("Processing your request. Please wait...")

    # Make the API request
    try:
        response = requests.get(API_BASE_URL, params={'url': message})
        data = response.json()

        # Check if the video exists
        if "result" in data and "url" in data["result"]:
            video_url = data["result"]["url"]
            video_title = data["result"]["title"]
            video_thumb = data["result"]["thumb"]

            # Send the video
            await update.message.reply_video(video_url, caption=f"Here's your video!\n\nTitle: {video_title}")
        else:
            await update.message.reply_text("Sorry, no media found in the provided URL.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

# Main function
def main():
    # Create an Application instance
    app = Application.builder().token(BOT_TOKEN).build()

    # Add command and message handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fetch_tiktok_media))

    # Start the bot
    app.run_polling()

if __name__ == "__main__":
    main()
