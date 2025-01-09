from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.constants import ParseMode
import requests

# Define the two APIs
API_1 = "https://tele-social.vercel.app/down?url="
API_2 = "https://api.smtv.uz/yt/?url="

# Function to handle start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send me a YouTube link, and I'll fetch videos from two different APIs!"
    )

# Function to process YouTube links
async def process_youtube_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.text:
        return

    youtube_url = update.message.text.strip()
    if "youtu" not in youtube_url:
        await update.message.reply_text("Please send a valid YouTube link!")
        return

    # Fetch from API 1
    api1_response = requests.get(f"{API_1}{youtube_url}")
    if api1_response.status_code == 200:
        api1_data = api1_response.json()
        video1_url = api1_data.get("video", "Not Available")
        video1_title = api1_data.get("title", "Unknown Title")
        video1_thumbnail = api1_data.get("thumb", "")

        text1 = f"**Title:** {video1_title}\n[Download Video]( {video1_url})"
        await update.message.reply_photo(photo=video1_thumbnail, caption=text1, parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text("Failed to fetch data from API 1!")

    # Fetch from API 2
    api2_response = requests.get(f"{API_2}{youtube_url}")
    if api2_response.status_code == 200:
        api2_data = api2_response.json()
        video2_url = api2_data["medias"][0].get("url", "Not Available")
        video2_title = api2_data.get("title", "Unknown Title")
        video2_thumbnail = api2_data.get("thumbnail", "")

        text2 = f"**Title:** {video2_title}\n[Download Video]( {video2_url})"
        await update.message.reply_photo(photo=video2_thumbnail, caption=text2, parse_mode=ParseMode.MARKDOWN)
    else:
        await update.message.reply_text("Failed to fetch data from API 2!")

# Main function to set up the bot
def main():
    # Replace 'YOUR_BOT_TOKEN' with your Telegram bot token
    application = ApplicationBuilder().token("8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM").build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", start))

    # Message handler
    application.add_handler(CommandHandler("message", process_youtube_link))

    application.run_polling()

if __name__ == "__main__":
    main()
