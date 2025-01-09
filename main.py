import logging
import requests
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

API_BASE_URL = "https://tele-social.vercel.app/down?url="

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the command /start is issued."""
    await update.message.reply_text("Welcome! Send me a social media link, and I'll download the media for you.")

def extract_media(data):
    """Extract media based on the platform."""
    platform = data.get("service") or data.get("platform")
    
    if platform == "snapchat":
        return extract_snapchat(data)
    elif platform == "TikTok":
        return extract_tiktok(data)
    else:
        return {"error": "Unsupported platform", "platform": platform}

def extract_snapchat(data):
    """Extract media data for Snapchat."""
    try:
        picker_data = data.get("picker", [])
        videos = [
            {
                "type": item.get("type", "unknown"),
                "url": item.get("url"),
                "thumbnail": item.get("thumb"),
            }
            for item in picker_data
        ]
        return videos
    except Exception as e:
        return {"error": "Failed to extract Snapchat data", "details": str(e)}

def extract_tiktok(data):
    """Extract media data for TikTok."""
    try:
        video_url = data["data"].get("video")
        audio_url = data["data"].get("audio")
        creator = {
            "username": data["creator"].get("username"),
            "name": data["creator"].get("name"),
            "profile_photo": data["creator"].get("profile_photo"),
        }
        details = {
            "total_views": data["details"].get("total_views"),
            "total_likes": data["details"].get("total_likes"),
            "total_comments": data["details"].get("total_comment"),
            "total_shares": data["details"].get("total_share"),
            "total_downloads": data["details"].get("total_download"),
            "video_duration": data["details"].get("video_duration"),
        }
        return {"video_url": video_url, "audio_url": audio_url, "creator": creator, "details": details}
    except Exception as e:
        return {"error": "Failed to extract TikTok data", "details": str(e)}

async def download_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle user messages containing links and process them using the API."""
    url = update.message.text.strip()
    await update.message.reply_text("Processing your link... Please wait.")

    try:
        # Query the API
        api_response = requests.get(f"{API_BASE_URL}{url}")
        response_data = api_response.json()

        if response_data.get("status") and response_data.get("data"):
            platform_data = extract_media(response_data["data"][0])

            # Handle media based on platform
            if isinstance(platform_data, dict) and "error" in platform_data:
                await update.message.reply_text(f"Error: {platform_data['error']}")
            elif "video_url" in platform_data:  # TikTok
                await handle_tiktok(update, platform_data)
            else:  # Snapchat
                await handle_snapchat(update, platform_data)
        else:
            await update.message.reply_text("Failed to retrieve media. Please check the link or try another one.")
    except Exception as e:
        logger.error(f"Error processing link: {e}")
        await update.message.reply_text("An error occurred while processing your request. Please try again later.")

async def handle_tiktok(update, platform_data):
    """Send TikTok media details to the user."""
    video_url = platform_data.get("video_url")
    audio_url = platform_data.get("audio_url")
    creator = platform_data.get("creator")
    details = platform_data.get("details")

    message = (
        f"🎥 TikTok Video:\n"
        f"👤 Creator: {creator['name']} (@{creator['username']})\n"
        f"👀 Views: {details['total_views']}\n"
        f"❤️ Likes: {details['total_likes']}\n"
        f"💬 Comments: {details['total_comments']}\n"
        f"🔗 [Download Video]({video_url})"
    )
    await update.message.reply_text(message, parse_mode="Markdown")

async def handle_snapchat(update, platform_data):
    """Send Snapchat media details to the user."""
    for video in platform_data:
        video_url = video["url"]
        thumbnail_url = video.get("thumbnail")
        if thumbnail_url:
            await update.message.reply_photo(photo=thumbnail_url, caption="Snapchat Media")
        await update.message.reply_text(f"🎥 [Download Snapchat Video]({video_url})", parse_mode="Markdown")

def main() -> None:
    """Run the bot."""
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    application = Application.builder().token("8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM").build()

    # Register command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_media))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
