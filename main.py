import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the API URL
API_URL = "https://tele-social.vercel.app/down?url="

# Define a function to handle the "/start" command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Send me a YouTube video link, and I'll download it for you.")

# Define a function to handle incoming messages
def download_video(update: Update, context: CallbackContext) -> None:
    url = update.message.text  # Get the link sent by the user
    if "youtu" in url:  # Check if the link contains 'youtube'
        # Send a request to the API to get video details
        response = requests.get(API_URL + url)
        
        if response.status_code == 200:
            data = response.json()
            
            if data['status']:  # If the response is valid
                video_url = data['video']  # Get the video URL
                video_title = data['title']  # Get the video title
                
                # Send the video to the user
                update.message.reply_text(f"Downloading: {video_title}")
                update.message.reply_video(video_url, caption=video_title)
            else:
                update.message.reply_text("Sorry, I couldn't fetch the video. Try another link.")
        else:
            update.message.reply_text("Error: Unable to reach the video server.")
    else:
        update.message.reply_text("Please send a valid YouTube URL.")

# Define a function to handle errors
def error(update: Update, context: CallbackContext) -> None:
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    # Replace with your Telegram bot's token
    TOKEN = '8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM'

    # Create the Updater and pass it your bot's token
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add handlers for commands and messages
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download_video))

    # Log all errors
    dispatcher.add_error_handler(error)

    # Start the bot
    updater.start_polling()

    # Run the bot until you send a signal to stop it
    updater.idle()

if __name__ == '__main__':
    main()
