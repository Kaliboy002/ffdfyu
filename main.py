import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Replace this with your Telegram bot token
BOT_TOKEN = "8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM"

# Facebook API Endpoint
FACEBOOK_API_URL = "https://super-api.wineclo.com/fb/?url="

# Start command handler
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Welcome to the Facebook Video Downloader Bot!\n"
        "Send me a Facebook video or reel link, and I'll download it for you."
    )

# Facebook video downloader handler
def download_facebook_video(update: Update, context: CallbackContext) -> None:
    video_url = update.message.text.strip()

    # Validate the URL
    if not video_url.startswith("http"):
        update.message.reply_text("Please send a valid Facebook video or reel link.")
        return

    try:
        # Call the API
        api_request_url = FACEBOOK_API_URL + video_url
        response = requests.get(api_request_url)

        # Check API response
        if response.status_code == 200:
            data = response.json()
            download_url = data.get("download_url")  # Get the video download URL

            if download_url:
                update.message.reply_text("Downloading your video... Please wait!")
                context.bot.send_document(chat_id=update.effective_chat.id, document=download_url)
            else:
                update.message.reply_text("Sorry, I couldn't fetch the video. Please try again.")
        else:
            update.message.reply_text("Failed to connect to the API. Please try again later.")
    except Exception as e:
        update.message.reply_text(f"An error occurred: {e}")

# Main function to start the bot
def main() -> None:
    # Create the updater and dispatcher
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Command and message handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download_facebook_video))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
