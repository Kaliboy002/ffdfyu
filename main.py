import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Your bot's token
BOT_TOKEN = "8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM"

# Function to download video from the API
def get_video_url(url: str):
    api_url = f"https://tele-social.vercel.app/down?url={url}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if data["status"]:
            return data.get("video")  # Returns the direct video URL
    return None

# Command to start the bot
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! Send me a YouTube video link and I'll download and send it to you.")

# Handle video links and send the video
def handle_video_link(update: Update, context: CallbackContext):
    url = update.message.text
    video_url = get_video_url(url)
    
    if video_url:
        update.message.reply_video(video_url)  # Send video directly to user
    else:
        update.message.reply_text("Sorry, I couldn't fetch the video. Please try again.")

# Main function to run the bot
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Command handler for /start
    dispatcher.add_handler(CommandHandler("start", start))
    
    # Handler for receiving messages (YouTube links)
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_video_link))
    
    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
