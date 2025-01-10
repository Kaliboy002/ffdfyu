import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Replace 'YOUR_BOT_TOKEN' with your Telegram Bot token
BOT_TOKEN = "8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM"

# API base URL
API_URL = "https://tele-social.vercel.app/down?url="

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command handler"""
    await update.message.reply_text("Hello! Send me a Facebook video link, and I'll download the video for you.")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle video link and download"""
    message = update.message.text.strip()
    
    if not message.startswith("http"):
        await update.message.reply_text("Please send a valid Facebook video URL.")
        return

    try:
        # Call the API to get video data
        response = requests.get(API_URL + message)
        data = response.json()

        if data.get("status") and data.get("data"):
            # Fetch the highest quality video URL
            video_data = data["data"][0]
            video_url = video_data["url"]
            thumbnail = video_data.get("thumbnail", "No thumbnail available")
            resolution = video_data.get("resolution", "Unknown resolution")

            # Send the video to the user
            await update.message.reply_video(video=video_url, caption=f"Resolution: {resolution}")
        else:
            await update.message.reply_text("Sorry, I couldn't download the video. Please check the link.")
    except Exception as e:
        logging.error(f"Error downloading video: {e}")
        await update.message.reply_text("An error occurred while processing the video.")

def main():
    """Start the bot"""
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    
    # Message handler for video links
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
