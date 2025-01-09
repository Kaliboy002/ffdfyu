import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the API URL for fetching video links
API_URL = "https://tele-social.vercel.app/down?url="

# Start command
async def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Send me a YouTube link, and I will fetch the video for you!')

# Function to handle YouTube links
async def handle_video(update: Update, context: CallbackContext) -> None:
    """Handle video download requests."""
    url = update.message.text
    if 'youtube' not in url:
        await update.message.reply_text("Please send a valid YouTube link!")
        return

    # Fetch video data using the API
    try:
        response = requests.get(API_URL + url)
        video_data = response.json()

        if video_data["status"]:
            video_url = video_data["video"]

            # Send the video file (from the video URL)
            await update.message.reply_video(video_url)

        else:
            await update.message.reply_text("Sorry, I couldn't fetch the video.")
    except Exception as e:
        logger.error(f"Error fetching video: {e}")
        await update.message.reply_text("An error occurred while fetching the video. Please try again.")

# Error handling for unknown errors
async def error(update: Update, context: CallbackContext) -> None:
    """Log the error and notify the user."""
    logger.warning(f'Update {update} caused error {context.error}')
    await update.message.reply_text('An error occurred. Please try again later.')

# Main function to run the bot
def main():
    """Start the bot."""
    # Your bot token
    TOKEN = '8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM'

    # Create the application
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_video))
    application.add_error_handler(error)

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()
