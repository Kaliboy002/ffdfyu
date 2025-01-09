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
    await update.message.reply_text("Hi! Send me a YouTube video link, and I will send you the video.")

# Function to handle incoming video link
async def handle_video_link(update: Update, context: CallbackContext) -> None:
    video_url = update.message.text
    logger.info(f"Received video URL: {video_url}")

    # API URL
    api_url = f"https://api.smtv.uz/yt/?url={video_url}"

    try:
        # Fetch video information from the API
        response = requests.get(api_url)
        logger.info(f"API Response: {response.status_code} - {response.text}")

        if response.status_code != 200:
            await update.message.reply_text("Failed to fetch data from the API.")
            return

        video_data = response.json()
        logger.info(f"Video data: {video_data}")

        # Check if the video data is valid and contains download link
        if video_data.get("error"):
            await update.message.reply_text("Sorry, there was an error processing the video.")
            return

        if "medias" in video_data and video_data["medias"]:
            video_info = video_data["medias"][0]
            video_link = video_info["url"]
            video_title = video_data.get("title", "No title available")
            video_thumbnail = video_data.get("thumbnail", "")

            logger.info(f"Video download link: {video_link}")

            # Download the video and send it
            video_response = requests.get(video_link, stream=True)
            video_file = video_response.raw

            # Send the video to the user
            await update.message.reply_video(video=video_file, caption=video_title, thumb=video_thumbnail)
        else:
            await update.message.reply_text("Sorry, I couldn't fetch the video download link.")
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
