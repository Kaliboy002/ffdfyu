import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Replace with your Telegram bot token
BOT_TOKEN = "8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM"

# API base URLs for Instagram downloader
PRIMARY_API_URL = "https://super-api.wineclo.com/instagram/?url="
SECONDARY_API_URL = "https://tele-social.vercel.app/down?url="

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

    # Try the primary API first
    try:
        response = requests.get(PRIMARY_API_URL + message)
        response.raise_for_status()
        data = response.json()

        # Check if videos or photos exist
        if data.get("video"):
            for video_url in data["video"]:
                await update.message.reply_video(video_url, caption="Here's your video!")
        elif data.get("photo"):
            for photo_url in data["photo"]:
                await update.message.reply_photo(photo_url, caption="Here's your photo!")
        else:
            raise ValueError("No media found in the primary API response.")
    except Exception as primary_error:
        await update.message.reply_text("Primary API failed. Trying the secondary API...")

        # Fallback to the secondary API
        try:
            response = requests.get(SECONDARY_API_URL + message)
            response.raise_for_status()
            data = response.json()

            if data.get("status") and data["status"] is True and "data" in data:
                for media in data["data"]:
                    if "url" in media:
                        await update.message.reply_video(media["url"], caption="Here's your media!")
            else:
                await update.message.reply_text("Sorry, no media found in the provided URL.")
        except Exception as secondary_error:
            await update.message.reply_text(f"Both APIs failed. Error: {str(secondary_error)}")

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
