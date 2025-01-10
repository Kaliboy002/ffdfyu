import logging
import os
import requests
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from yt_dlp import YoutubeDL

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
DOWNLOAD_DIR = "repository/Youtube"
SAVEFROM_API = "https://api.savefrom.net/api/convert"
MAXIMUM_DOWNLOAD_SIZE_MB = 2000  # 2 GB

# Ensure the download directory exists
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)


async def start(update: Update, context: CallbackContext) -> None:
    """Start command handler."""
    await update.message.reply_text("Hi! Send me a YouTube video link, and I will fetch the video for you.")


async def handle_video_link(update: Update, context: CallbackContext) -> None:
    """Handles incoming YouTube video links."""
    video_url = update.message.text.strip()
    logger.info(f"Received video URL: {video_url}")

    try:
        # Use SaveFrom API to fetch video data
        video_data = fetch_savefrom_data(video_url)
        if video_data:
            video_link = video_data["url"]
            video_title = video_data["title"]
            await send_video(update, video_link, video_title)
        else:
            # If API fails, fallback to yt-dlp
            await download_with_yt_dlp(update, video_url)
    except Exception as e:
        logger.error(f"Error processing video link: {e}")
        await update.message.reply_text("An error occurred. Please try again with a valid YouTube link.")


def fetch_savefrom_data(video_url: str) -> dict:
    """Fetch video details from SaveFrom.net API."""
    try:
        response = requests.post(SAVEFROM_API, json={"url": video_url}, timeout=20)
        if response.status_code == 200:
            result = response.json()
            # Check if the response contains valid video data
            if result.get("url"):
                return {
                    "url": result["url"],
                    "title": result.get("meta", {}).get("title", "Untitled"),
                }
    except Exception as e:
        logger.error(f"SaveFrom API error: {e}")
    return None


async def send_video(update: Update, video_link: str, title: str) -> None:
    """Downloads and sends the video."""
    try:
        # Download video using requests
        response = requests.get(video_link, stream=True)
        if response.status_code == 200:
            file_path = os.path.join(DOWNLOAD_DIR, "video.mp4")
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024 * 1024):  # 1 MB chunks
                    f.write(chunk)

            # Check file size
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
            if file_size_mb > MAXIMUM_DOWNLOAD_SIZE_MB:
                await update.message.reply_text("The video is too large to send via Telegram.")
                os.remove(file_path)
                return

            # Send the video to the user
            with open(file_path, "rb") as video_file:
                await update.message.reply_video(video=video_file, caption=title)

            # Clean up
            os.remove(file_path)
        else:
            await update.message.reply_text("Failed to download the video.")
    except Exception as e:
        logger.error(f"Error sending video: {e}")
        await update.message.reply_text("An error occurred while sending the video.")


async def download_with_yt_dlp(update: Update, video_url: str) -> None:
    """Fallback to downloading video using yt-dlp."""
    await update.message.reply_text("Attempting to download the video directly...")

    ydl_opts = {
        "format": "best",
        "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
        "quiet": True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            video_path = ydl.prepare_filename(info)
            video_title = info.get("title", "Downloaded Video")

        # Send downloaded video
        with open(video_path, "rb") as video_file:
            await update.message.reply_video(video=video_file, caption=video_title)

        # Clean up
        os.remove(video_path)

    except Exception as e:
        logger.error(f"Error downloading with yt-dlp: {e}")
        await update.message.reply_text("Failed to download the video using yt-dlp.")


def main() -> None:
    """Start the bot."""
    token = "8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM"  # Replace with your bot token
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_video_link))

    application.run_polling()


if __name__ == "__main__":
    main()
