import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from mega import Mega
import os
import tempfile

# Replace with your Telegram bot token
BOT_TOKEN = "8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM"

# API base URL for YouTube downloader
API_BASE_URL = "https://api.smtv.uz/yt/?url="

# MEGA credentials
MEGA_EMAIL = "shokrullahmohammadi072@gmail.com"
MEGA_PASSWORD = "SHM14002022SHM"

# Start command handler
async def start(update: Update, context):
    await update.message.reply_text("Welcome! Send me a YouTube URL, and I'll fetch the video for you.")

# Function to process YouTube URL
async def fetch_youtube_media(update: Update, context):
    message = update.message.text
    if "youtube.com" not in message and "youtu.be" not in message:
        await update.message.reply_text("Please send a valid YouTube URL.")
        return

    await update.message.reply_text("Processing your request. Please wait...")

    # Make the API request to get the video URL
    try:
        response = requests.get(API_BASE_URL, params={'url': message})
        data = response.json()

        # Check if the video exists and we have a download link
        if "medias" in data and len(data["medias"]) > 0:
            video_url = data["medias"][0]["url"]
            video_title = data["title"]

            # Download the video
            video_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
            with requests.get(video_url, stream=True) as video_response:
                video_response.raise_for_status()
                with open(video_file.name, "wb") as f:
                    for chunk in video_response.iter_content(chunk_size=8192):
                        f.write(chunk)

            # Login to MEGA
            mega = Mega()
            m = mega.login(MEGA_EMAIL, MEGA_PASSWORD)

            # Upload the video to MEGA
            file = m.upload(video_file.name)

            # Send the video file to the user
            with open(video_file.name, "rb") as video:
                await update.message.reply_video(
                    video,
                    caption=f"Here's your video: {video_title}"
                )

            # Clean up the downloaded video file
            os.remove(video_file.name)
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

    # Start the bot
    app.run_polling()

if __name__ == "__main__":
    main()
