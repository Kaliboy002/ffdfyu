import logging
import os
import hashlib
import requests
from telegram import Update, InputFile, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from yt_dlp import YoutubeDL

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
MAXIMUM_DOWNLOAD_SIZE_MB = 1000
DOWNLOAD_DIR = 'repository/Youtube'
API_URL_1 = "https://api.smtv.uz/yt/?url={}"
API_URL_2 = "https://tele-social.vercel.app/down?url={}"

# Ensure download directory exists
if not os.path.isdir(DOWNLOAD_DIR):
    os.mkdir(DOWNLOAD_DIR)


def get_file_path(url, format_id, extension):
    url_hash = hashlib.blake2b((url + format_id + extension).encode()).hexdigest()
    filename = f"{url_hash}.{extension}"
    return os.path.join(DOWNLOAD_DIR, filename)


async def start(update: Update, context: CallbackContext) -> None:
    """Start command handler."""
    await update.message.reply_text("Hi! Send me a YouTube video link, and I will try to fetch the video for you.")


async def handle_video_link(update: Update, context: CallbackContext) -> None:
    """Handles incoming YouTube video links."""
    video_url = update.message.text.strip()
    logger.info(f"Received video URL: {video_url}")

    try:
        # First API
        response_1 = requests.get(API_URL_1.format(video_url), timeout=15)
        if response_1.status_code == 200:
            video_data_1 = response_1.json()
            if video_data_1 and not video_data_1.get("error") and "medias" in video_data_1:
                video_link = video_data_1["medias"][0]["url"]
                video_title = video_data_1.get("title", "Untitled")
                thumbnail = video_data_1.get("thumbnail")
                await send_video(update, video_link, video_title, thumbnail)
                return

        # Second API
        response_2 = requests.get(API_URL_2.format(video_url), timeout=15)
        if response_2.status_code == 200:
            video_data_2 = response_2.json()
            if video_data_2 and video_data_2.get("status"):
                video_link = video_data_2["video"]
                video_title = video_data_2.get("title", "Untitled")
                await send_video(update, video_link, video_title)
                return

        # If APIs fail, fallback to manual download
        await download_with_yt_dlp(update, video_url)

    except Exception as e:
        logger.error(f"Error fetching video: {e}")
        await update.message.reply_text("An error occurred while processing your request. Please try again.")


async def send_video(update: Update, video_link: str, title: str, thumbnail: str = None) -> None:
    """Downloads and sends the video."""
    try:
        # Download the video
        video_response = requests.get(video_link, stream=True)
        if video_response.status_code == 200:
            video_file = InputFile(video_response.raw, filename="video.mp4")
            await update.message.reply_video(video=video_file, caption=title, thumb=thumbnail)
        else:
            await update.message.reply_text("Failed to download the video.")
    except Exception as e:
        logger.error(f"Error sending video: {e}")
        await update.message.reply_text("An error occurred while sending the video.")


async def download_with_yt_dlp(update: Update, video_url: str) -> None:
    """Fallback to downloading video using yt-dlp."""
    await update.message.reply_text("Attempting to download the video directly...")

    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
        'quiet': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            video_path = ydl.prepare_filename(info)
            video_title = info.get('title', 'Downloaded Video')
            duration = info.get('duration', 0)
            thumbnail_url = info.get('thumbnail')

        # Send downloaded video
        with open(video_path, 'rb') as video_file:
            thumbnail = None
            if thumbnail_url:
                thumbnail_response = requests.get(thumbnail_url)
                if thumbnail_response.status_code == 200:
                    thumbnail = InputMediaPhoto(thumbnail_response.raw)
            await update.message.reply_video(video=video_file, caption=video_title, thumb=thumbnail)

        # Cleanup
        os.remove(video_path)

    except Exception as e:
        logger.error(f"Error downloading with yt-dlp: {e}")
        await update.message.reply_text("Failed to download the video using yt-dlp.")


# Main function to run the bot
def main() -> None:
    token = '8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM'
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_video_link))

    application.run_polling()


if __name__ == '__main__':
    main()
