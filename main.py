import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os

# Replace with your Telegram bot token
BOT_TOKEN = "8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM"

# API base URL for Snapchat downloader
API_BASE_URL = "https://tele-social.vercel.app/down?url="

# Start command handler
async def start(update: Update, context):
    await update.message.reply_text("Welcome! Send me a Snapchat media link, and I'll fetch it for you.")

# Function to process Snapchat media URL
async def fetch_snapchat_media(update: Update, context):
    message = update.message.text
    if "snapchat.com" not in message:
        await update.message.reply_text("Please send a valid Snapchat URL.")
        return

    await update.message.reply_text("Processing your request. Please wait...")

    # Make the API request to get media data
    try:
        # Build the full API URL
        response = requests.get(API_BASE_URL + message)
        data = response.json()

        # Check if the media exists and we have a download link
        if data["status"] is False:
            await update.message.reply_text(f"Error: {data['Message']}")
            return
        
        # Check if video media type is present
        for media in data["Message"]["picker"]:
            if media["type"] == "video":
                video_url = media["url"]
                video_thumb = media["thumb"]

                # Download the video
                video_file = "downloaded_snapchat_video.mp4"
                with requests.get(video_url, stream=True) as video_response:
                    video_response.raise_for_status()
                    with open(video_file, "wb") as f:
                        for chunk in video_response.iter_content(chunk_size=8192):
                            f.write(chunk)

                # Send the video to the user
                with open(video_file, "rb") as video:
                    await update.message.reply_video(
                        video,
                        caption="Here's your Snapchat media!"
                    )

                # Clean up the downloaded file
                os.remove(video_file)
                return

        # If no video found
        await update.message.reply_text("No video media found in the provided Snapchat URL.")
        
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

# Main function
def main():
    # Create an Application instance
    app = Application.builder().token(BOT_TOKEN).build()

    # Add command and message handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fetch_snapchat_media))

    # Start the bot
    app.run_polling()

if __name__ == "__main__":
    main()
