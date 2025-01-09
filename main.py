import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to handle the /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome! Send a YouTube video link, and I will send you the download link.')

# Function to handle video download
def download_video(update: Update, context: CallbackContext) -> None:
    video_url = update.message.text
    if "https://youtu.be/" not in video_url:
        update.message.reply_text("Please send a valid YouTube link.")
        return

    # Call the API to get the video info
    api_url = f"https://tele-social.vercel.app/down?url={video_url}"
    response = requests.get(api_url)
    data = response.json()

    if data["status"]:
        video_link = data["video"]
        update.message.reply_text(f"Here is your download link: {video_link}")
    else:
        update.message.reply_text("Sorry, I couldn't fetch the video. Please try again later.")

def main():
    # Your bot token from BotFather
    token = '8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM'

    # Create the Updater and pass it your bot's token
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add handlers for start command and message (to handle video URL)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download_video))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop
    updater.idle()

if __name__ == '__main__':
    main()
