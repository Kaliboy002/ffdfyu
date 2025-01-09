import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to start the bot
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Hi! Send me a video link, and I will send you the video.")

# Function to handle incoming video link
async def handle_video_link(update: Update, context: CallbackContext) -> None:
    video_url = update.message.text
    # Extract video ID from the URL (assuming the format "https://youtu.be/{video_id}")
    video_id = video_url.split("youtu.be/")[1].split("?")[0]
    # API URL
    api_url = f"https://tele-social.vercel.app/down?url={video_url}"

    # Fetch video information
    try:
        response = requests.get(api_url)
        video_data = response.json()

        # Extract video download link
        if video_data["status"]:
            video_link = video_data["video"]

            # Download the video and send it
            video_response = requests.get(video_link, stream=True)
            video_file = video_response.raw

            # Send the video to the user
            await update.message.reply_video(video=video_file, caption=video_data["title"])
        else:
            await update.message.reply_text("Sorry, I couldn't fetch the video.")
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("An error occurred while processing the video.")

# Main function to run the bot
def main() -> None:
    # Your bot's token
    token = '8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM'

    # Set up the Application (replaces Updater)
    application = Application.builder().token(token).build()

    # Add handlers for commands and messages
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_video_link))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
