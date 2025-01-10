import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os

# Replace with your Telegram bot token
BOT_TOKEN = "8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM"

# API base URLs
YOUTUBE_API_BASE_URL = "https://api.smtv.uz/yt/?url="
TWITTER_API_BASE_URL = "https://super-api.wineclo.com/twitter/?url="
TELE_SERVICE_API_URL = "https://tele-social.vercel.app/down?url="
TIKTOK_API_BASE_URL = "https://api.smtv.uz/yt/?url="  # TikTok API URL (same as YouTube)

# Start command handler
async def start(update: Update, context):
    await update.message.reply_text("Welcome! Send me a URL from YouTube, Twitter, TikTok, or Pinterest, and I'll fetch the video for you.")

# Function to process URLs and determine the platform
async def fetch_media(update: Update, context):
    message = update.message.text

    if "youtube.com" in message or "youtu.be" in message:
        await fetch_youtube_media(update, context, message)
    elif "twitter.com" in message:
        await fetch_twitter_media(update, context, message)
    elif "tiktok.com" in message:
        await fetch_tiktok_media(update, context, message)
    elif "pinterest.com" in message:
        await fetch_pinterest_media(update, context, message)
    else:
        await update.message.reply_text("Please send a valid URL from YouTube, Twitter, TikTok, or Pinterest.")

# Function to process YouTube URL
async def fetch_youtube_media(update: Update, context, url):
    await update.message.reply_text("Processing your YouTube request. Please wait...")

    try:
        response = requests.get(YOUTUBE_API_BASE_URL, params={'url': url})
        data = response.json()

        if "medias" in data and len(data["medias"]) > 0:
            video_url = data["medias"][0]["url"]
            video_title = data["title"]

            video_file = "downloaded_video.mp4"
            with requests.get(video_url, stream=True) as video_response:
                video_response.raise_for_status()
                with open(video_file, "wb") as f:
                    for chunk in video_response.iter_content(chunk_size=8192):
                        f.write(chunk)

            with open(video_file, "rb") as video:
                await update.message.reply_video(
                    video,
                    caption=f"Here's your YouTube video!\n\nTitle: {video_title}"
                )

            os.remove(video_file)
        else:
            await update.message.reply_text("No media found in the provided YouTube URL.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

# Function to process Twitter URL
async def fetch_twitter_media(update: Update, context, url):
    await update.message.reply_text("Processing your Twitter request. Please wait...")

    try:
        response = requests.get(TWITTER_API_BASE_URL, params={'url': url})
        data = response.json()

        if "result" in data and "url" in data["result"]:
            video_url = data["result"]["url"]
            video_title = data["result"]["title"]

            video_file = "downloaded_video.mp4"
            with requests.get(video_url, stream=True) as video_response:
                video_response.raise_for_status()
                with open(video_file, "wb") as f:
                    for chunk in video_response.iter_content(chunk_size=8192):
                        f.write(chunk)

            with open(video_file, "rb") as video:
                await update.message.reply_video(
                    video,
                    caption=f"Here's your Twitter video!\n\nTitle: {video_title}"
                )

            os.remove(video_file)
        else:
            await update.message.reply_text("No media found in the provided Twitter URL.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

# Function to process TikTok URL
async def fetch_tiktok_media(update: Update, context, url):
    await update.message.reply_text("Processing your TikTok request. Please wait...")

    try:
        response = requests.get(TIKTOK_API_BASE_URL, params={'url': url})
        data = response.json()

        if "medias" in data and len(data["medias"]) > 0:
            video_url = data["medias"][0]["url"]
            video_title = data["title"]

            video_file = "downloaded_video.mp4"
            with requests.get(video_url, stream=True) as video_response:
                video_response.raise_for_status()
                with open(video_file, "wb") as f:
                    for chunk in video_response.iter_content(chunk_size=8192):
                        f.write(chunk)

            with open(video_file, "rb") as video:
                await update.message.reply_video(
                    video,
                    caption=f"Here's your TikTok video!\n\nTitle: {video_title}"
                )

            os.remove(video_file)
        else:
            await update.message.reply_text("No media found in the provided TikTok URL.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

# Function to process Pinterest URL
async def fetch_pinterest_media(update: Update, context, url):
    await update.message.reply_text("Processing your Pinterest request. Please wait...")

    try:
        response = requests.get(TELE_SERVICE_API_URL, params={'url': url})
        data = response.json()

        if "result" in data and "url" in data["result"]:
            video_url = data["result"]["url"]
            video_title = data["result"]["title"]

            video_file = "downloaded_video.mp4"
            with requests.get(video_url, stream=True) as video_response:
                video_response.raise_for_status()
                with open(video_file, "wb") as f:
                    for chunk in video_response.iter_content(chunk_size=8192):
                        f.write(chunk)

            with open(video_file, "rb") as video:
                await update.message.reply_video(
                    video,
                    caption=f"Here's your Pinterest video!\n\nTitle: {video_title}"
                )

            os.remove(video_file)
        else:
            await update.message.reply_text("No media found in the provided Pinterest URL.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

# Main function
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fetch_media))

    app.run_polling()

if __name__ == "__main__":
    main()
