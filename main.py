import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import io

# Replace with your Telegram bot token
BOT_TOKEN = "8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM"

# API base URL for YouTube downloader
API_BASE_URL = "https://api.smtv.uz/yt/?url="

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

    # Make the API request
    try:
        response = requests.get(API_BASE_URL, params={'url': message})
        data = response.json()

        # Check if the video exists and we have a download link
        if "medias" in data and len(data["medias"]) > 0:
            video_url = data["medias"][0]["url"]
            video_title = data["title"]

            # Download the video (stream it in chunks)
            video_stream = requests.get(video_url, stream=True)
            video_stream.raise_for_status()

            # Use io.BytesIO to handle the video as a file-like object in memory
            video_file = io.BytesIO()

            # Write the video to the in-memory file in chunks to save memory
            for chunk in video_stream.iter_content(chunk_size=8192):
                video_file.write(chunk)

            # Reset the pointer to the start of the video file
            video_file.seek(0)

            # Send the video to the user
            await update.message.reply_video(
                video_file,
                caption=f"Here's your video!\n\nTitle: {video_title}"
            )

            # Close the in-memory file
            video_file.close()

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
