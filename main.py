import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging for debugging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to handle the /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! Send me a YouTube video link and I will download it for you.')

# Function to handle the downloading process
def download_video(update: Update, context: CallbackContext) -> None:
    url = update.message.text.strip()

    # Check if the link is from YouTube
    if 'youtu' in url:
        api_url = f"https://tele-social.vercel.app/down?url={url}"
        
        try:
            # Send the request to the API
            response = requests.get(api_url)
            video_data = response.json()
            
            # Check if the API response is valid
            if video_data.get("status"):
                video_url = video_data.get("video")
                video_title = video_data.get("title")
                
                # Send the video to the user
                update.message.reply_text(f"Downloading: {video_title}")
                update.message.reply_video(video_url, caption=video_title)
            else:
                update.message.reply_text("Sorry, I couldn't fetch the video. Please try again.")
        except Exception as e:
            update.message.reply_text("An error occurred while fetching the video.")
            logger.error(f"Error: {e}")
    else:
        update.message.reply_text("Please send a valid YouTube link.")

# Main function to set up the bot
def main():
    # Create an Updater object with your bot token
    updater = Updater("8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register the handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download_video))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
