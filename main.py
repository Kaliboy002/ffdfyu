import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import requests

# Set up logging to capture errors or important events
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Your Telegram Bot token here
TELEGRAM_TOKEN = '8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM'

# API URL to get the video information
API_URL = 'https://tele-social.vercel.app/down?url={}'


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hello! Send me a Facebook link to get video resolutions.')


async def fetch_video_data(update: Update, context: CallbackContext) -> None:
    try:
        url = " ".join(context.args)  # Getting the URL passed by the user
        if not url:
            await update.message.reply_text('Please provide a valid Facebook video URL.')
            return

        # Making a request to the API with the provided URL
        api_response = requests.get(API_URL.format(url))
        data = api_response.json()

        if data['status']:
            # Prepare and send the video data to the user
            response_text = f"Video found on Facebook:\n\nPlatform: {data['platform']}\n"
            for video in data['data']:
                response_text += f"Resolution: {video['resolution']}\n"
                response_text += f"Thumbnail: {video['thumbnail']}\n"
                response_text += f"Download Link: {video['url']}\n\n"

            await update.message.reply_text(response_text)
        else:
            await update.message.reply_text('No video data found for this URL.')
    except Exception as e:
        await update.message.reply_text('An error occurred while fetching video data.')
        logger.error(f"Error fetching video data: {e}")


def main() -> None:
    # Set up the Application and Dispatcher
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Register the handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get_video", fetch_video_data))

    # Start the bot
    application.run_polling()


if __name__ == '__main__':
    main()
