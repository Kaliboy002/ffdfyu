import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to start the bot
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Hi! Send me a YouTube video link, and I will send you the video.")

# Function to fetch video using Tele-Social API
async def fetch_video_from_tele_social(video_url: str):
    api_url = f"https://tele-social.vercel.app/down?url={video_url}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            video_data = response.json()
            if video_data.get("status"):
                return video_data["video"], video_data.get("title", "No Title")
        else:
            logger.error(f"Tele-Social API error: {response.status_code}")
            return None, None
    except Exception as e:
        logger.error(f"Error in Tele-Social API: {e}")
        return None, None

# Function to fetch video using SMTV API
async def fetch_video_from_smtv(video_url: str):
    api_url = f"https://api.smtv.uz/yt/?url={video_url}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            video_data = response.json()
            if "medias" in video_data and video_data["medias"]:
                video_info = video_data["medias"][0]
                return video_info["url"], video_data.get("title", "No Title"), video_data.get("thumbnail", "")
        else:
            logger.error(f"SMTV API error: {response.status_code}")
            return None, None, None
    except Exception as e:
        logger.error(f"Error in SMTV API: {e}")
        return None, None, None

# Function to handle incoming video link
async def handle_video_link(update: Update, context: CallbackContext) -> None:
    video_url = update.message.text.strip()
    logger.info(f"Received video URL: {video_url}")

    # Check if the URL is valid YouTube URL
    if "youtube.com" not in video_url and "youtu.be" not in video_url:
        await update.message.reply_text("Invalid YouTube URL. Please try again.")
        return

    # Try fetching video from Tele-Social API
    video_link, video_title = await fetch_video_from_tele_social(video_url)
    if video_link:
        logger.info(f"Video fetched from Tele-Social API: {video_link}")
        # Download and send the video from Tele-Social
        video_response = requests.get(video_link, stream=True)
        video_file = video_response.raw
        await update.message.reply_video(video=video_file, caption=video_title)
        return

    # If Tele-Social API fails, try fetching from SMTV API
    video_link, video_title, video_thumbnail = await fetch_video_from_smtv(video_url)
    if video_link:
        logger.info(f"Video fetched from SMTV API: {video_link}")
        # Download and send the video from SMTV
        video_response = requests.get(video_link, stream=True)
        video_file = video_response.raw
        await update.message.reply_video(video=video_file, caption=video_title, thumb=video_thumbnail)
        return

    # If both APIs fail, inform the user
    await update.message.reply_text("Sorry, I couldn't fetch the video. Please try again later.")

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
