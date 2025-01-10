import logging
import requests
from telegram import Update, InputFile, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Function to process video links
async def process_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    video_url = update.message.text.strip()

    # Validate the input URL
    if "facebook.com" not in video_url:
        await update.message.reply_text("Please send a valid Facebook video link.")
        return

    # API call to fetch video details
    api_url = f"https://super-api.wineclo.com/fb/?url={video_url}"
    try:
        response = requests.get(api_url)
        response_data = response.json()

        # Check if the API returned a valid result
        if "result" in response_data:
            video_data = response_data["result"]
            video_download_url = video_data["url"]
            video_title = video_data["title"]
            thumbnail_url = video_data["thumb"]

            # Send video details with download link
            buttons = [
                [InlineKeyboardButton("Download Video", url=video_download_url)]
            ]
            await update.message.reply_photo(
                photo=thumbnail_url,
                caption=f"🎥 *Title:* {video_title}\n\nClick below to download the video:",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        else:
            await update.message.reply_text("❌ Failed to fetch video details. Please try another link.")
    except Exception as e:
        logger.error(f"Error fetching video: {e}")
        await update.message.reply_text("❌ An error occurred while processing the video.")

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me a Facebook video link, and I'll fetch it for you!")

# Main function to run the bot
def main():
    bot_token = "8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM"
    app = ApplicationBuilder().token(bot_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_video))

    logger.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
