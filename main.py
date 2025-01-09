import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import time

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

    # Try first API
    api_url_1 = f"https://api.smtv.uz/yt/?url={video_url}"
    api_url_2 = f"https://tele-social.vercel.app/down?url={video_url}"

    try:
        # First, check with the first API
        start_time = time.time()
        response_1 = requests.get(api_url_1)
        logger.info(f"API 1 Response: {response_1.status_code} - {response_1.text}")
        api_1_duration = time.time() - start_time

        if response_1.status_code == 200:
            video_data_1 = response_1.json()
            if not video_data_1.get("error") and "medias" in video_data_1 and video_data_1["medias"]:
                video_link = video_data_1["medias"][0]["url"]
                video_title = video_data_1.get("title", "No title available")
                video_thumbnail = video_data_1.get("thumbnail", "")
                logger.info(f"Video download link from API 1: {video_link}")

                # Send the video from API 1
                video_response = requests.get(video_link, stream=True)
                video_file = video_response.raw
                await update.message.reply_video(video=video_file, caption=video_title, thumb=video_thumbnail)
                return  # Successfully handled video from API 1

        # If API 1 fails, try the second API
        start_time = time.time()
        response_2 = requests.get(api_url_2)
        logger.info(f"API 2 Response: {response_2.status_code} - {response_2.text}")
        api_2_duration = time.time() - start_time

        if response_2.status_code == 200:
            video_data_2 = response_2.json()
            if video_data_2.get("status"):
                video_link = video_data_2["video"]
                video_title = video_data_2.get("title", "No title available")
                logger.info(f"Video download link from API 2: {video_link}")

                # Send the video from API 2
                video_response = requests.get(video_link, stream=True)
                video_file = video_response.raw
                await update.message.reply_video(video=video_file, caption=video_title)
                return  # Successfully handled video from API 2

        # If both APIs fail
        await update.message.reply_text("Sorry, I couldn't fetch the video from either API.")
        
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
