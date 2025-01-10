import requests
from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Telegram bot token
BOT_TOKEN = "8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM"

# API Endpoint for Facebook video download
FACEBOOK_API_URL = "https://super-api.wineclo.com/fb/?url="

# Command to start the bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Welcome! Send me a Facebook video link, and I'll download the video for you."
    )

# Handle messages with Facebook video links
def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    chat_id = update.message.chat_id

    # Check if the message is a valid URL
    if user_message.startswith("http"):
        update.message.reply_text("Processing your link... Please wait.")

        # Fetch the video download link
        response = requests.get(FACEBOOK_API_URL + user_message)
        if response.status_code == 200:
            data = response.json()

            # Check if the API returned a valid video URL
            if "result" in data and "url" in data["result"]:
                video_url = data["result"]["url"]
                title = data["result"].get("title", "Here is your video!")

                # Send the video to the user
                update.message.reply_video(video=video_url, caption=title)
            else:
                update.message.reply_text(
                    "Failed to fetch the video. Please ensure the link is valid."
                )
        else:
            update.message.reply_text("Error connecting to the video download API.")
    else:
        update.message.reply_text("Please send a valid Facebook video link.")

# Main function to start the bot
def main():
    # Create the Updater and pass it your bot's token
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register the start command handler
    dp.add_handler(CommandHandler("start", start))

    # Register a message handler for video links
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl+C
    updater.idle()

if __name__ == "__main__":
    main()
