import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to handle /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Send me a YouTube link, and I\'ll send you the video!')

# Function to download and send video
def download_video(update: Update, context: CallbackContext) -> None:
    url = update.message.text.strip()
    
    # Construct the API endpoint URL
    api_url = f"https://tele-social.vercel.app/down?url={url}"
    
    try:
        # Make a request to the API to get video information
        response = requests.get(api_url)
        data = response.json()

        # Check if the response is valid
        if data.get("status"):
            video_url = data.get("video")
            video_stream = requests.get(video_url, stream=True)

            # Send the video file
            update.message.reply_video(video_stream.raw)
        else:
            update.message.reply_text('Sorry, I couldn\'t fetch the video. Please check the link.')
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        update.message.reply_text('An error occurred. Please try again later.')

def main() -> None:
    """Start the bot."""
    # Insert your bot token here
    bot_token = '8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM'
    
    updater = Updater(bot_token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download_video))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
