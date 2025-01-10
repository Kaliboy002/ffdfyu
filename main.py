import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import pymongo
import gridfs
from io import BytesIO

# Replace with your Telegram bot token
BOT_TOKEN = "8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM"

# API base URL for YouTube downloader
API_BASE_URL = "https://api.smtv.uz/yt/?url="

# MongoDB connection setup (Use your connection string here)
MONGO_URI = "mongodb+srv://mrshokrullah:L7yjtsOjHzGBhaSR@cluster0.aqxyz.mongodb.net/shah?retryWrites=true&w=majority&appName=Cluster0"  # or your MongoDB Atlas URI
DB_NAME = "video_db"

# Connect to MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
fs = gridfs.GridFS(db)

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

            # Download the video into a BytesIO stream
            video_file = BytesIO()
            with requests.get(video_url, stream=True) as video_response:
                video_response.raise_for_status()
                for chunk in video_response.iter_content(chunk_size=8192):
                    video_file.write(chunk)

            # Reset the file pointer to the beginning of the file
            video_file.seek(0)

            # Upload the video to MongoDB using GridFS
            file_id = fs.put(video_file, filename=f"{video_title}.mp4")

            # Send confirmation that video is uploaded
            await update.message.reply_text(f"Video uploaded successfully to the cloud!\n\nTitle: {video_title}")

            # Now, send the video to the user from MongoDB
            grid_out = fs.get(file_id)
            await update.message.reply_video(
                grid_out, caption=f"Here's your video!\n\nTitle: {video_title}"
            )

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
