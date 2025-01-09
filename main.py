import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Define the URL for the video download API
API_URL = "https://tele-social.vercel.app/down?url="

# Function to start the bot
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Send me a YouTube video link, and I'll send you the download link!")

# Function to handle the video download command
def download_video(update: Update, context: CallbackContext):
    # Get the YouTube URL from the user's message
    url = ' '.join(context.args)
    
    if not url:
        update.message.reply_text("Please provide a YouTube link!")
        return
    
    # Call the API to get video info
    response = requests.get(API_URL + url)
    
    # Check if the response is successful
    if response.status_code == 200:
        data = response.json()
        
        if data['status']:
            video_url = data['video']
            update.message.reply_text(f"Here is your video download link: {video_url}")
        else:
            update.message.reply_text("Sorry, I couldn't fetch the video. Please check the link.")
    else:
        update.message.reply_text("Something went wrong, please try again later.")

# Set up the Telegram bot
def main():
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    updater = Updater("8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM", use_context=True)
    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("download", download_video))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
