import logging
import requests
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

API_BASE_URL = "https://tele-social.vercel.app/down?url="

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the command /start is issued."""
    await update.message.reply_text("Welcome! Send me a social media link, and I'll download the media for you.")

async def download_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle user messages containing links and process them using the API."""
    url = update.message.text.strip()
    await update.message.reply_text("Processing your link... Please wait.")

    try:
        # Query the API
        api_response = requests.get(f"{API_BASE_URL}{url}")
        response_data = api_response.json()

        # Check if the API returned a valid response
        if response_data.get("status") and response_data.get("data"):
            media_info = response_data["data"][0]
            video_url = media_info["url"]
            thumbnail_url = media_info.get("thumbnail", None)

            # Send the media to the user
            if thumbnail_url:
                await update.message.reply_photo(photo=thumbnail_url, caption=f"Downloading: {url}")
            video_response = requests.get(video_url, stream=True)
            video_filename = "downloaded_video.mp4"
            with open(video_filename, "wb") as f:
                f.write(video_response.content)
            with open(video_filename, "rb") as f:
                await update.message.reply_video(video=InputFile(f))
        else:
            await update.message.reply_text("Failed to retrieve media. Please check the link or try another one.")
    except Exception as e:
        logger.error(f"Error processing link: {e}")
        await update.message.reply_text("An error occurred while processing your request. Please try again later.")

def main() -> None:
    """Run the bot."""
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    application = Application.builder().token("8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM").build()

    # Register command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_media))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
