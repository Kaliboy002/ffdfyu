import requests
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Function to fetch video data from the first API
def fetch_video_from_api1(url):
    api_url = f"https://tele-social.vercel.app/down?url={url}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    return None

# Function to fetch video data from the second API
def fetch_video_from_api2(url):
    api_url = f"https://api.smtv.uz/yt/?url={url}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    return None

# Handler function for start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Send me a YouTube video link, and I will fetch video links for you!")

# Handler function for processing YouTube links
def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    if "youtu" in user_message:  # Simple check for YouTube links
        update.message.reply_text("Fetching video data...")
        
        # Fetch data from both APIs
        data_api1 = fetch_video_from_api1(user_message)
        data_api2 = fetch_video_from_api2(user_message)
        
        # Prepare response for API1
        if data_api1 and data_api1.get("status"):
            video_link_api1 = data_api1.get("video", "Not available")
            video_hd_link_api1 = data_api1.get("video_hd", "Not available")
            update.message.reply_text(
                f"*API 1 Results:*\n"
                f"Title: {data_api1.get('title', 'N/A')}\n"
                f"Channel: {data_api1.get('channel', 'N/A')}\n"
                f"[Standard Quality]({video_link_api1})\n"
                f"[HD Quality]({video_hd_link_api1})",
                parse_mode=ParseMode.MARKDOWN,
            )
        else:
            update.message.reply_text("Failed to fetch data from API 1.")
        
        # Prepare response for API2
        if data_api2 and not data_api2.get("error"):
            medias = data_api2.get("medias", [])
            if medias:
                video_link_api2 = medias[0].get("url", "Not available")
                update.message.reply_text(
                    f"*API 2 Results:*\n"
                    f"Title: {data_api2.get('title', 'N/A')}\n"
                    f"Author: {data_api2.get('author', 'N/A')}\n"
                    f"[Video Link]({video_link_api2})",
                    parse_mode=ParseMode.MARKDOWN,
                )
            else:
                update.message.reply_text("No video links available in API 2 response.")
        else:
            update.message.reply_text("Failed to fetch data from API 2.")
    else:
        update.message.reply_text("Please send a valid YouTube link!")

# Main function to run the bot
def main():
    # Replace YOUR_BOT_TOKEN with your actual Telegram bot token
    updater = Updater("8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM", use_context=True)
    
    # Command handlers
    updater.dispatcher.add_handler(CommandHandler("start", start))
    
    # Message handler for YouTube links
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
