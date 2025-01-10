import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

API_TOKEN = '8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM'  # Replace with your bot's API token

# Function to get Facebook video data
def get_video_data(fb_url):
    api_url = f"https://tele-social.vercel.app/down?url={fb_url}"
    response = requests.get(api_url)
    return response.json()

# Function to handle the '/video' command
def video(update: Update, context: CallbackContext):
    # Get the Facebook URL from the command arguments
    if len(context.args) == 0:
        update.message.reply_text("Please provide a Facebook URL.")
        return
    
    fb_url = context.args[0]
    
    # Fetch video data from the API
    video_data = get_video_data(fb_url)
    
    if video_data.get("status"):
        # If video data is available, send video to the user
        video_info = video_data["data"][0]  # Select the highest quality video (720p)
        video_url = video_info["url"]
        thumbnail_url = video_info["thumbnail"]
        
        # Send video and thumbnail to the user
        update.message.reply_text("Here is your video:", reply_markup=None)
        update.message.reply_video(video_url, caption="Video", thumb=thumbnail_url)
    else:
        update.message.reply_text("Sorry, the video could not be retrieved.")

# Main function to start the bot
def main():
    updater = Updater(API_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    # Add command handler for the '/video' command
    dispatcher.add_handler(CommandHandler("video", video))
    
    # Start polling updates
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
