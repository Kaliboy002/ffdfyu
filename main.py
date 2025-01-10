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
    await update.message.reply_text("Hi! Send me a Facebook video link, and I will send you the video.")

# Function to handle incoming video link
async def handle_video_link(update: Update, context: CallbackContext) -> None:
    video_url = update.message.text
    logger.info(f"Received video URL: {video_url}")

    # First API URL
    api_url_1 = f"https://super-api.wineclo.com/fb/?url={video_url}"

    # Second API URL (fallback)
    api_url_2 = f"https://tele-social.vercel.app/down?url={video_url}"

    try:
        # Try first API
        response = requests.get(api_url_1)
        logger.info(f"API 1 Response: {response.status_code} - {response.text}")

        if response.status_code == 200:
            video_data = response.json()
            logger.info(f"Video data from API 1: {video_data}")

            if "result" in video_data and video_data["result"]:
                video_link = video_data["result"]["url"]
                video_title = video_data["result"]["title"]
                video_thumbnail = video_data["result"]["thumb"]

                logger.info(f"Video download link from API 1: {video_link}")

                # Download the video and send it
                video_response = requests.get(video_link, stream=True)
                if video_response.status_code == 200:
                    video_file = video_response.raw
                    await update.message.reply_video(video=video_file, caption=video_title, thumb=video_thumbnail)
                    return  # Exit after sending the video
                else:
                    logger.error(f"Failed to download video from API 1: {video_response.status_code}")
                    await update.message.reply_text("Failed to download the video from the first API.")
                    return

        # If the first API fails, try the second API
        logger.info(f"Trying second API: {api_url_2}")
        response = requests.get(api_url_2)
        logger.info(f"API 2 Response: {response.status_code} - {response.text}")

        if response.status_code == 200:
            video_data = response.json()
            logger.info(f"Video data from API 2: {video_data}")

            if video_data.get("status") and "data" in video_data and video_data["data"]:
                video_link = video_data["data"][0]["url"]
                video_title = "Facebook Video"
                video_thumbnail = video_data["data"][0]["thumbnail"]

                logger.info(f"Video download link from API 2: {video_link}")

                # Download the video and send it
                video_response = requests.get(video_link, stream=True)
                if video_response.status_code == 200:
                    video_file = video_response.raw
                    await update.message.reply_video(video=video_file, caption=video_title, thumb=video_thumbnail)
                    return  # Exit after sending the video
                else:
                    logger.error(f"Failed to download video from API 2: {video_response.status_code}")
                    await update.message.reply_text("Failed to download the video from the second API.")
                    return
            else:
                logger.error("No valid video data found in API 2 response.")
                await update.message.reply_text("No video data found in the second API response.")
        else:
            logger.error(f"API 2 failed: {response.status_code} - {response.text}")
            await update.message.reply_text("Failed to fetch data from the second API.")

    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {e}")
        await update.message.reply_text("An error occurred while processing the video link.")

    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("An unexpected error occurred while processing the video.")

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
