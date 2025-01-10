import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Replace with your Telegram bot token
BOT_TOKEN = "8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM"

# API base URL for Instagram downloader
API_BASE_URL = "https://super-api.wineclo.com/instagram/?url="

# Start command handler
async def start(update: Update, context):
    await update.message.reply_text("Welcome! Send me an Instagram URL, and I'll fetch the video or photo for you.")

# Function to process Instagram URL
async def fetch_instagram_media(update: Update, context):
    message = update.message.text
    if "instagram.com" not in message:
        await update.message.reply_text("Please send a valid Instagram URL.")
        return

    await update.message.reply_text("Processing your request. Please wait...")

    # Make the API request
    try:
        response = requests.get(API_BASE_URL + message)
        data = response.json()

        # Check if videos or photos exist
        if data.get("video"):
            for video_url in data["video"]:
                await update.message.reply_video(video_url, caption="Here's your video!")
        elif data.get("photo"):
            for photo_url in data["photo"]:
                await update.message.reply_photo(photo_url, caption="Here's your photo!")
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
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fetch_instagram_media))

    # Start the bot
    app.run_polling()

if __name__ == "__main__":
    main()
