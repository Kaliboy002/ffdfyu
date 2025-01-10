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

    # Extract video ID from the URL (supporting both "youtu.be" and "youtube.com")
    try:
        if "youtu.be" in video_url:
            video_id = video_url.split("youtu.be/")[1].split("?")[0]
        elif "youtube.com" in video_url and "v=" in video_url:
            video_id = video_url.split("v=")[1].split("&")[0]
        else:
            await update.message.reply_text("Invalid YouTube URL format.")
            return
    except IndexError:
        await update.message.reply_text("Invalid YouTube URL format.")
        return

    logger.info(f"Extracted video ID: {video_id}")

    # Primary API URL
    api_url_1 = f"https://tele-social.vercel.app/down?url={video_url}"
    # Fallback API URL
    api_url_2 = f"https://api.smtv.uz/yt/?url={video_url}"

    try:
        # Try first API
        response = requests.get(api_url_1)
        logger.info(f"API 1 Response: {response.status_code} - {response.text}")

        if response.status_code == 200:
            video_data = response.json()
            logger.info(f"Video data from API 1: {video_data}")

            if video_data.get("status"):
                video_link = video_data["video"]
                logger.info(f"Video download link from API 1: {video_link}")

                # Download the video and send it
                video_response = requests.get(video_link, stream=True)
                video_file = video_response.raw

                # Send the video to the user
                await update.message.reply_video(video=video_file, caption=video_data["title"])
                return  # Exit after sending the video

        # If the first API fails, try the second API
        response = requests.get(api_url_2)
        logger.info(f"API 2 Response: {response.status_code} - {response.text}")

        if response.status_code == 200:
            video_data = response.json()
            logger.info(f"Video data from API 2: {video_data}")

            if video_data.get("error"):
                await update.message.reply_text("Sorry, there was an error processing the video.")
                return

            if "medias" in video_data and video_data["medias"]:
                video_info = video_data["medias"][0]
                video_link = video_info["url"]
                video_title = video_data.get("title", "No title available")
                video_thumbnail = video_data.get("thumbnail", "")

                logger.info(f"Video download link from API 2: {video_link}")

                # Download the video and send it
                video_response = requests.get(video_link, stream=True)
                video_file = video_response.raw

                # Send the video to the user
                await update.message.reply_video(video=video_file, caption=video_title, thumb=video_thumbnail)
                return  # Exit after sending the video

        else:
            await update.message.reply_text("Failed to fetch data from both APIs.")
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
    main()    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
