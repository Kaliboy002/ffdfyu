import requests
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Telegram bot token
BOT_TOKEN = "8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM"

# API Endpoint for Facebook video download
FACEBOOK_API_URL = "https://super-api.wineclo.com/fb/?url="


# Command to start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Welcome! Send me a Facebook video link, and I'll download the video for you."
    )


# Handle messages with Facebook video links
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text

    # Check if the message is a valid URL
    if user_message.startswith("http"):
        await update.message.reply_text("Processing your link... Please wait.")

        # Fetch the video download link
        response = requests.get(FACEBOOK_API_URL + user_message)
        if response.status_code == 200:
            data = response.json()

            # Check if the API returned a valid video URL
            if "result" in data and "url" in data["result"]:
                video_url = data["result"]["url"]
                title = data["result"].get("title", "Here is your video!")

                # Send the video to the user
                await update.message.reply_video(video=video_url, caption=title)
            else:
                await update.message.reply_text(
                    "Failed to fetch the video. Please ensure the link is valid."
                )
        else:
            await update.message.reply_text("Error connecting to the video download API.")
    else:
        await update.message.reply_text("Please send a valid Facebook video link.")


# Main function to start the bot
def main():
    # Create the Application and pass it your bot's token
    application = Application.builder().token(BOT_TOKEN).build()

    # Register the start command handler
    application.add_handler(CommandHandler("start", start))

    # Register a message handler for video links
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    application.run_polling()


if __name__ == "__main__":
    main()
