import logging
import requests
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import time

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to start the bot
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Hi! Send me a YouTube video link, and I will try to fetch the video for you.")

# Function to handle video links
async def handle_video_link(update: Update, context: CallbackContext) -> None:
    video_url = update.message.text.strip()
    logger.info(f"Received video URL: {video_url}")

    api_url_1 = f"https://api.smtv.uz/yt/?url={video_url}"
    api_url_2 = f"https://tele-social.vercel.app/down?url={video_url}"

    try:
        # First API
        response_1 = requests.get(api_url_1, timeout=15)
        if response_1.status_code == 200:
            video_data_1 = response_1.json()
            if video_data_1 and not video_data_1.get("error") and "medias" in video_data_1:
                video_link = video_data_1["medias"][0]["url"]
                video_title = video_data_1.get("title", "Untitled")
                await send_video(update, video_link, video_title, video_data_1.get("thumbnail"))
                return

        # Second API
        response_2 = requests.get(api_url_2, timeout=15)
        if response_2.status_code == 200:
            video_data_2 = response_2.json()
            if video_data_2 and video_data_2.get("status"):
                video_link = video_data_2["video"]
                video_title = video_data_2.get("title", "Untitled")
                await send_video(update, video_link, video_title)
                return

        # If both APIs fail
        await update.message.reply_text("Sorry, I couldn't fetch the video from either API.")

    except Exception as e:
        logger.error(f"Error fetching video: {e}")
        await update.message.reply_text("An error occurred while processing your request. Please try again.")

# Function to send video
async def send_video(update: Update, video_link: str, title: str, thumbnail: str = None) -> None:
    try:
        # Download the video file
        video_response = requests.get(video_link, stream=True)
        if video_response.status_code == 200:
            video_file = InputFile(video_response.raw, filename="video.mp4")
            await update.message.reply_video(video=video_file, caption=title, thumb=thumbnail)
        else:
            await update.message.reply_text("Failed to download the video.")
    except Exception as e:
        logger.error(f"Error sending video: {e}")
        await update.message.reply_text("An error occurred while sending the video.")

# Main function to run the bot
def main() -> None:
    # Your bot token
    token = '8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM'

    # Set up the Application
    application = Application.builder().token(token).build()

    # Add handlers for commands and messages
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_video_link))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
