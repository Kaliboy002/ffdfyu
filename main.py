import logging
import requests
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Function to process video links
async def process_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

            # Download the video
            video_content = requests.get(video_download_url)
            if video_content.status_code == 200:
                with open("video.mp4", "wb") as f:
                    f.write(video_content.content)

                # Send the video file
                with open("video.mp4", "rb") as video_file:
                    await update.message.reply_video(
                        video=video_file,
                        caption=f"🎥 *Title:* {video_title}",
                        parse_mode="Markdown"
                    )
            else:
                await update.message.reply_text("❌ Failed to download the video. Please try another link.")
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
    bot_token = "YOUR_BOT_TOKEN"
    app = ApplicationBuilder().token(bot_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_video))

    logger.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
