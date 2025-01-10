import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from io import BytesIO

# Enable logging for debugging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Your Telegram bot token here
TOKEN = "8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM"

# API URL to fetch video details from
API_URL = "https://api.smtv.uz/yt/?url="

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Send me a YouTube video link, and I'll send you the video!")

def fetch_video_url(video_url: str) -> str:
    """Fetch video download link using the provided API."""
    response = requests.get(API_URL + video_url)
    data = response.json()
    
    if data["error"]:
        return None

    # Assuming we want to download the first available video stream
    video_url = data["medias"][0]["url"]
    return video_url

def send_video(update: Update, context: CallbackContext) -> None:
    """Receive a YouTube URL and send the video to the user."""
    video_url = update.message.text.strip()

    # Fetch the download URL from the API
    download_url = fetch_video_url(video_url)
    
    if download_url:
        # Download the video content
        video_response = requests.get(download_url)
        video_data = BytesIO(video_response.content)

        # Send the video to the user
        update.message.reply_video(video_data)
    else:
        update.message.reply_text("Sorry, I couldn't fetch the video. Please check the link.")

def main():
    """Start the bot."""
    updater = Updater(TOKEN, use_context=True)

    # Register handlers
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(None, send_video))  # Filters removed due to older version

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
