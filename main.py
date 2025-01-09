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
    await update.message.reply_text(
        "Welcome! Send me a TikTok or Instagram link, and I'll download the media for you."
    )

async def download_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle user messages containing links and process them using the API."""
    url = update.message.text.strip()
    await update.message.reply_text("Processing your link... Please wait.")

    try:
        # Query the API
        response = requests.get(f"{API_BASE_URL}{url}")
        if response.status_code != 200:
            await update.message.reply_text("Failed to fetch data from the API. Please try again later.")
            return

        data = response.json()
        if not data.get("status"):
            await update.message.reply_text("Invalid link or unsupported platform. Please try again.")
            return

        platform = data.get("platform", "Unknown Platform")
        media_data = data.get("data")
        
        if platform == "TikTok" and media_data:
            video_url = media_data.get("video")
            if video_url:
                video_response = requests.get(video_url, stream=True)
                if video_response.status_code == 200:
                    with open("tiktok_video.mp4", "wb") as file:
                        file.write(video_response.content)
                    with open("tiktok_video.mp4", "rb") as file:
                        await update.message.reply_video(video=InputFile(file), caption="Here is your TikTok video!")
                else:
                    await update.message.reply_text("Failed to download the video. Please try again.")
            else:
                await update.message.reply_text("No video URL found in the response. Please check the link.")

        elif platform == "Instagram" and media_data:
            media_item = media_data[0]  # Use the first media item in the list
            video_url = media_item.get("url")
            thumbnail_url = media_item.get("thumbnail")
            if thumbnail_url:
                await update.message.reply_photo(photo=thumbnail_url, caption="Media Thumbnail")
            if video_url:
                video_response = requests.get(video_url, stream=True)
                if video_response.status_code == 200:
                    with open("instagram_video.mp4", "wb") as file:
                        file.write(video_response.content)
                    with open("instagram_video.mp4", "rb") as file:
                        await update.message.reply_video(video=InputFile(file), caption="Here is your Instagram video!")
                else:
                    await update.message.reply_text("Failed to download the video. Please try again.")
            else:
                await update.message.reply_text("No video URL found in the response. Please check the link.")

        else:
            await update.message.reply_text("Unsupported platform or no media found. Please try a different link.")

    except Exception as e:
        logger.error(f"Error processing link: {e}")
        await update.message.reply_text("An error occurred while processing your request. Please try again later.")

def main() -> None:
    """Run the bot."""
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    application = Application.builder().token("YOUR_BOT_TOKEN").build()

    # Register command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_media))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
