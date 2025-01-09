import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
import json

# Enable logging for debugging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to handle the /start command
async def start(update: Update, context) -> None:
    await update.message.reply_text('Hi! Send me a YouTube video link, and I will help you download it.')

# Function to handle the downloading process
async def download_video(update: Update, context) -> None:
    url = update.message.text.strip()

    # Check if the link is from YouTube
    if 'youtu' in url:
        api_url = f"https://tele-social.vercel.app/down?url={url}"
        
        try:
            # Send the request to the API
            response = requests.get(api_url)
            video_data = response.json()

            # Check if the API response is valid
            if video_data.get("status"):
                video_title = video_data.get("title")
                video_thumb = video_data.get("thumb")
                video_url = video_data.get("video")
                video_hd_url = video_data.get("video_hd")
                audio_url = video_data.get("audio")
                quality = video_data.get("quality")

                # Send video details to the user
                await update.message.reply_text(f"Video Title: {video_title}\nQuality: {quality}")

                # Display thumbnail
                await update.message.reply_photo(video_thumb, caption=f"Video Thumbnail: {video_title}")

                # Create inline keyboard with options to download
                keyboard = [
                    [
                        InlineKeyboardButton("Download Video (360p/720p)", callback_data=f"video_{video_url}"),
                        InlineKeyboardButton("Download HD Video", callback_data=f"video_hd_{video_hd_url}"),
                    ],
                    [InlineKeyboardButton("Download Audio", callback_data=f"audio_{audio_url}")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await update.message.reply_text("Choose an option to download:", reply_markup=reply_markup)
            else:
                await update.message.reply_text("Sorry, I couldn't fetch the video. Please try again.")
        except Exception as e:
            await update.message.reply_text("An error occurred while fetching the video.")
            logger.error(f"Error: {e}")
    else:
        await update.message.reply_text("Please send a valid YouTube link.")

# Function to handle callback queries (user's download choice)
async def button(update: Update, context) -> None:
    query = update.callback_query
    await query.answer()

    choice = query.data.split("_")
    download_type = choice[0]
    file_url = choice[1]

    if download_type == "video":
        await query.edit_message_text(text="Sending video...")
        await query.message.reply_video(file_url)
    elif download_type == "video_hd":
        await query.edit_message_text(text="Sending HD video...")
        await query.message.reply_video(file_url)
    elif download_type == "audio":
        await query.edit_message_text(text="Sending audio...")
        await query.message.reply_audio(file_url)

# Main function to set up the bot
def main():
    # Create an Application object with your bot token
    application = Application.builder().token("8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM").build()

    # Register the handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    application.add_handler(CallbackQueryHandler(button))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
