import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Define your API URL format
API_URL = "https://tele-social.vercel.app/down?url="

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome! Send me a YouTube URL, and I\'ll fetch the video or audio for you.')

def download_video(update: Update, context: CallbackContext) -> None:
    url = update.message.text.strip()
    if 'youtu' in url:
        api_url = f"{API_URL}{url}"

        try:
            # Make the request to the API
            response = requests.get(api_url)
            video_data = response.json()

            # Check if the response has valid data
            if video_data.get("status"):
                title = video_data.get("title")
                thumb = video_data.get("thumb")
                video_url = video_data.get("video")
                video_hd_url = video_data.get("video_hd")
                audio_url = video_data.get("audio")
                quality = video_data.get("quality")

                # Send title and thumbnail
                update.message.reply_text(f"Video Title: {title}\nQuality: {quality}")
                update.message.reply_photo(thumb, caption=f"Thumbnail for: {title}")

                # Provide download options via inline keyboard
                keyboard = [
                    [InlineKeyboardButton("Download Video (360p/720p)", callback_data=f"video_{video_url}"),
                     InlineKeyboardButton("Download HD Video", callback_data=f"video_hd_{video_hd_url}")],
                    [InlineKeyboardButton("Download Audio", callback_data=f"audio_{audio_url}")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.message.reply_text("Choose an option to download:", reply_markup=reply_markup)

            else:
                update.message.reply_text("Sorry, I couldn't fetch the video. Please try again.")
        except Exception as e:
            logger.error(f"Error: {e}")
            update.message.reply_text("An error occurred while fetching the video.")
    else:
        update.message.reply_text("Please send a valid YouTube URL.")

def handle_download_choice(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    data = query.data.split('_')

    if data[0] == 'video':
        video_url = data[1]
        query.message.reply_text("Downloading video...")
        query.message.reply_video(video_url, caption="Here's your video!")

    elif data[0] == 'video_hd':
        video_hd_url = data[1]
        query.message.reply_text("Downloading HD video...")
        query.message.reply_video(video_hd_url, caption="Here's your HD video!")

    elif data[0] == 'audio':
        audio_url = data[1]
        query.message.reply_text("Downloading audio...")
        query.message.reply_audio(audio_url, caption="Here's your audio!")

def main() -> None:
    # Set up the Updater and Dispatcher
    updater = Updater("8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM")
    dispatcher = updater.dispatcher

    # Add command and message handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download_video))
    dispatcher.add_handler(CallbackQueryHandler(handle_download_choice))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
