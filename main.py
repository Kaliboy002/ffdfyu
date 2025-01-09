import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, CallbackContext, filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Define your API URL format
API_URL = "https://tele-social.vercel.app/down?url="

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Welcome! Send me a YouTube URL, and I\'ll fetch the video or audio for you.')

async def download_video(update: Update, context: CallbackContext) -> None:
    url = update.message.text.strip()
    if 'youtu' in url:
        api_url = f"{API_URL}{url}"

        try:
            # Make the request to the API
            response = requests.get(api_url)
            video_data = response.json()

            # Check if the response has valid data
            if video_data.get("status"):
                video_url = video_data.get("video")
                video_hd_url = video_data.get("video_hd")
                audio_url = video_data.get("audio")

                # Send the video or audio directly to the user
                if video_url:
                    await update.message.reply_video(video_url, caption="Here's your video!")
                elif video_hd_url:
                    await update.message.reply_video(video_hd_url, caption="Here's your HD video!")
                elif audio_url:
                    await update.message.reply_audio(audio_url, caption="Here's your audio!")

            else:
                await update.message.reply_text("Sorry, I couldn't fetch the video. Please try again.")
        except Exception as e:
            logger.error(f"Error: {e}")
            await update.message.reply_text("An error occurred while fetching the video.")
    else:
        await update.message.reply_text("Please send a valid YouTube URL.")

def main() -> None:
    # Set up the Application
    application = Application.builder().token("8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM").build()

    # Add command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
