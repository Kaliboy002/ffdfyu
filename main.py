import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os

# Replace with your Telegram bot token
BOT_TOKEN = "8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM"

# API base URLs
PRIMARY_API_BASE_URL = "https://tele-social.vercel.app/down?url="  # Primary API changed to Tele service
FALLBACK_API_BASE_URL = "https://api.smtv.uz/yt/"  # Fallback to smtv.uz API

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

    # Try the primary API (Tele service)
    try:
        response = requests.get(PRIMARY_API_BASE_URL + message)
        data = response.json()

        if data.get("status") and "video" in data:
            video_url = data["video"]
            video_title = data["title"]
        else:
            raise Exception("No media found in the primary API response.")

    except Exception as primary_error:
        # If the primary API fails, use the fallback API (smtv.uz)
        try:
            response = requests.get(FALLBACK_API_BASE_URL, params={'url': message})
            data = response.json()

            if "medias" in data and len(data["medias"]) > 0:
                video_url = data["medias"][0]["url"]
                video_title = data["title"]
            else:
                raise Exception("No media found in the fallback API response.")

        except Exception as fallback_error:
            await update.message.reply_text(
                f"An error occurred while processing your request.\n"
                f"Primary API Error: {primary_error}\n"
                f"Fallback API Error: {fallback_error}"
            )
            return

    # Download and send the video
    try:
        video_file = "downloaded_video.mp4"
        with requests.get(video_url, stream=True) as video_response:
            video_response.raise_for_status()
            with open(video_file, "wb") as f:
                for chunk in video_response.iter_content(chunk_size=8192):
                    f.write(chunk)

        with open(video_file, "rb") as video:
            await update.message.reply_video(
                video,
                caption=f"Here's your video!\n\nTitle: {video_title}"
            )

        os.remove(video_file)

    except Exception as e:
        await update.message.reply_text(f"Failed to download or send the video: {str(e)}")

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
