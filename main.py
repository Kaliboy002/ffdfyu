import os
import re
import logging
import hashlib
import requests
from functools import lru_cache
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import yt_dlp as YoutubeDL

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

class YoutubeDownloader:
    MAXIMUM_DOWNLOAD_SIZE_MB = 1000  # Limit for direct downloads
    DOWNLOAD_DIR = "repository/Youtube"

    @staticmethod
    def initialize():
        # Check if the directory exists; if not, create it.
        if not os.path.isdir(YoutubeDownloader.DOWNLOAD_DIR):
            os.makedirs(YoutubeDownloader.DOWNLOAD_DIR)  # This ensures that parent directories are created if needed.

    @staticmethod
    def is_youtube_link(url):
        youtube_patterns = [
            r'(https?\:\/\/)?youtube\.com\/shorts\/([a-zA-Z0-9_-]{11}).*',
            r'(https?\:\/\/)?www\.youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})(?!.*list=)',
            r'(https?\:\/\/)?youtu\.be\/([a-zA-Z0-9_-]{11})(?!.*list=)',
        ]
        for pattern in youtube_patterns:
            if re.match(pattern, url):
                return True
        return False

    @lru_cache(maxsize=128)
    def get_file_path(url, format_id, extension):
        # Generate a unique file name based on the URL and format ID
        hashed_url = hashlib.blake2b((url + format_id + extension).encode()).hexdigest()
        filename = f"{hashed_url}.{extension}"
        return os.path.join(YoutubeDownloader.DOWNLOAD_DIR, filename)

    @staticmethod
    def _get_formats(url):
        ydl_opts = {'listformats': True, 'quiet': True}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        return info['formats']

    @staticmethod
    def download_video(url, format_id, file_path):
        ydl_opts = {'format': format_id, 'outtmpl': file_path, 'quiet': True}
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hi! Send me a YouTube video link, and I will send you the downloaded video.")

async def handle_video_link(update: Update, context: CallbackContext):
    video_url = update.message.text.strip()
    logger.info(f"Received video URL: {video_url}")

    if not YoutubeDownloader.is_youtube_link(video_url):
        await update.message.reply_text("Invalid YouTube URL. Please try again.")
        return

    # If the link is valid, use yt-dlp to get formats and download the video
    formats = YoutubeDownloader._get_formats(video_url)
    best_format = formats[-1]  # Assuming the last format is the best
    file_path = YoutubeDownloader.get_file_path(video_url, best_format['format_id'], best_format['ext'])

    try:
        if not os.path.isfile(file_path):  # Download only if file doesn't exist
            YoutubeDownloader.download_video(video_url, best_format['format_id'], file_path)

        with open(file_path, 'rb') as video_file:
            await update.message.reply_video(video=video_file, caption="Here is your downloaded video!")
    except Exception as e:
        logger.error(f"Error during download: {e}")
        await update.message.reply_text("An error occurred while processing the video.")

def main():
    token = "8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM"  # Replace with your actual bot token
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_video_link))

    application.run_polling()

if __name__ == '__main__':
    YoutubeDownloader.initialize()
    main()
