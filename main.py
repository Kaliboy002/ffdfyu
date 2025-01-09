import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Set up logging to track errors
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to handle the /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome! Send me a YouTube video link and I will send you the download link.')

# Function to handle video download request
def download_video(update: Update, context: CallbackContext) -> None:
    video_url = update.message.text.split(" ", 1)[1]
    
    if not video_url:
        update.message.reply_text("Please provide a valid YouTube video URL.")
        return

    api_url = f"https://tele-social.vercel.app/down?url={video_url}"
    
    try:
        # Request to get the video data
        response = requests.get(api_url)
        data = response.json()

        if data['status']:
            video_link = data.get('video', '')
            if video_link:
                # Send the video to the user
                update.message.reply_video(video=video_link)
            else:
                update.message.reply_text("Sorry, I couldn't retrieve the video.")
        else:
            update.message.reply_text("Failed to download the video. Please check the URL.")
    
    except Exception as e:
        logger.error(f"Error downloading video: {e}")
        update.message.reply_text("An error occurred while processing the video request. Please try again later.")

def main() -> None:
    # Set up the Telegram bot with your token
    updater = Updater("8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add handlers for commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("download", download_video))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
