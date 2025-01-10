import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os

# Replace with your Telegram bot token
BOT_TOKEN = "YOUR_BOT_TOKEN"

# API Base URLs
YOUTUBE_API_URL = "https://api.smtv.uz/yt/?url="
TWITTER_API_URL = "https://super-api.wineclo.com/twitter/?url="
TIKTOK_API_URL = "https://api.smtv.uz/tiktok/?url="
PINTEREST_API_URL = "https://api.smtv.uz/pin/?url="
FACEBOOK_API_URL = "https://api.smtv.uz/fb/?url="
INSTAGRAM_API_URL = "https://api.smtv.uz/ig/?url="

# Start command handler
async def start(update: Update, context):
    await update.message.reply_text("Welcome! Send me a URL from YouTube, Twitter, TikTok, Pinterest, Facebook, or Instagram, and I'll fetch the media for you.")

# Function to handle YouTube URLs
async def fetch_youtube_media(update: Update, context):
    message = update.message.text
    if "youtube.com" not in message and "youtu.be" not in message:
        await update.message.reply_text("Please send a valid YouTube URL.")
        return

    await update.message.reply_text("Processing your request. Please wait...")

    try:
        response = requests.get(YOUTUBE_API_URL, params={'url': message})
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
                await update.message.reply_video(video, caption=f"Here's your video!\n\nTitle: {video_title}")

            os.remove(video_file)
        else:
            await update.message.reply_text("Sorry, no media found in the provided URL.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

# Function to handle Twitter URLs
async def fetch_twitter_media(update: Update, context):
    message = update.message.text
    if "twitter.com" not in message:
        await update.message.reply_text("Please send a valid Twitter URL.")
        return

    await update.message.reply_text("Processing your request. Please wait...")

    try:
        response = requests.get(TWITTER_API_URL, params={'url': message})
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
                await update.message.reply_video(video, caption=f"Here's your video!\n\nTitle: {video_title}")

            os.remove(video_file)
        else:
            await update.message.reply_text("No media found in the provided URL.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

# Function to handle TikTok URLs
async def fetch_tiktok_media(update: Update, context):
    message = update.message.text
    if "tiktok.com" not in message:
        await update.message.reply_text("Please send a valid TikTok URL.")
        return

    await update.message.reply_text("Processing your request. Please wait...")

    try:
        response = requests.get(TIKTOK_API_URL, params={'url': message})
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
                await update.message.reply_video(video, caption=f"Here's your video!\n\nTitle: {video_title}")

            os.remove(video_file)
        else:
            await update.message.reply_text("Sorry, no media found in the provided URL.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

# Function to handle Pinterest URLs
async def fetch_pinterest_media(update: Update, context):
    message = update.message.text
    if "pinterest.com" not in message:
        await update.message.reply_text("Please send a valid Pinterest URL.")
        return

    await update.message.reply_text("Processing your request. Please wait...")

    try:
        response = requests.get(PINTEREST_API_URL, params={'url': message})
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
                await update.message.reply_video(video, caption=f"Here's your video!\n\nTitle: {video_title}")

            os.remove(video_file)
        else:
            await update.message.reply_text("Sorry, no media found in the provided URL.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

# Main function
def main():
    # Create an Application instance
    app = Application.builder().token(BOT_TOKEN).build()

    # Add command and message handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fetch_youtube_media))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fetch_twitter_media))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fetch_tiktok_media))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fetch_pinterest_media))

    # Start the bot
    app.run_polling()

if __name__ == "__main__":
    main()
