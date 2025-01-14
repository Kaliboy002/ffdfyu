from pyrogram import Client, types, filters, enums
import asyncio
import os
import requests
import json
from pymongo import MongoClient

# MongoDB Connection
client = MongoClient('mongodb+srv://mrshokrullah:L7yjtsOjHzGBhaSR@cluster0.aqxyz.mongodb.net/shah?retryWrites=true&w=majority&appName=Cluster0')  # Use your MongoDB URI here
db = client['shah']  # Create a database
users_collection = db['shm']  # Create a collection for users

# Bot Config Objects
class Config:
    SESSION = "BQG0lX0AqA8ehJYDUzT99Yo_Zh7H4hkEuAc1L9nETnK7pShNlxfCHxFjSCNgNR6a6oik70m8-OD2GgMzTo2F0v-tmONXkPU5qUuAZKDaj0_d6z6zMFQ_nenj0FmbRtpaF_C-ao_7VFdSqCEuPkiDeuTCSg4EK6PZF7iQ5hnuQSVsbAAzLJj_EaWcONGOk-EImSj5Dp_bHkVaXrEMX7FTH_t5qU71SCvNpmHPzQMdag1u9EBdUcMZ_s49pKobk-nNSIDTOUPxtOxUEcQ2XLyqvvweWjXnTXJPdNYa1JJb4P9xDtaS9GpAdQ6GMBItrqOwPCszLc84_GIAKKoEgHHRo1H0Df71PQAAAAGkAOGhAA"
    API_KEY = "7628087790:AAHuxIiUigcgYsxl6GP6Gcg327dMfctu364"
    API_HASH = "e51a3154d2e0c45e5ed70251d68382de"
    API_ID = 15787995
    SUDO = 7046488481
    CHANNLS = ['Kali_Linux_BOTS']
    FORCE_SUBSCRIBE = True  # Default Force Subscribe Mode
    API_BASE_URL = "https://super-api.wineclo.com/instagram/?url="  # Instagram API Base URL

# Ensure required directories and files exist
if not os.path.exists('./.session'):
    os.mkdir('./.session')

if not os.path.exists('./data.json'):
    json.dump({'users': [], 'languages': {}}, open('./data.json', 'w'), indent=3)

# Initialize Pyrogram Client
app = Client(
    "./.session/bot",
    bot_token=Config.API_KEY,
    api_hash=Config.API_HASH,
    api_id=Config.API_ID,
    parse_mode=enums.ParseMode.DEFAULT
)

# Language Texts
LANGUAGE_TEXTS = {
    "en": {
        "welcome": "<b><i>Welcome to IG Media Downloader!</b></i>\n\n✈️ You can easily download Instagram <b>photos and videos</b> of any user with high quality and speed⚡\n\n<b>⁀➴ Just send me the Instagram URL 🖇️🙂</b>",
        "join_channel": "⚠️<b><i> To use this bot, you must first join our Telegram channel</i></b>\n\nAfter successfully joining, click the 🔐𝗝𝗼𝗶𝗻𝗲𝗱 button to confirm your bot membership and to continue.",
        "verify_join": "🔐𝗝𝗼𝗶𝗻𝗲𝗱",
        "join_channel_btn": "Jᴏɪɴ ᴄʜᴀɴɴᴇʟ⚡️",
        "not_joined": "🤨 You are not a member of our channel. Please join and try again.",
        "downloading": "<b>Downloading, please wait</b>...⏳🙃",
        "download_successful": "<b>Download completed successfully</b> ✈️",
        "error": "✗ Sorry, there was an issue while downloading 💔\nPlease check the link and try again ⚡"
    },
    "fa": {
        "welcome": "<b>به ربات دانلودر اینستاگرام خوش آمدید!</b>\n\n✈️ شما می‌توانید به‌راحتی<b> عکس‌ها و ویدیوهای اینستاگرام </b>را با کیفیت و سرعت بالا دانلود کنید⚡\n\n<b>✦ کافیست لینک آن پست را برای من ارسال کنید 🖇️🙂</b>",
        "join_channel": (
            "<b>⚠️ برای استفاده از این ربات، نخست شما باید به کانال‌ های زیر عضو گردید</b>.\n\n"
            "در غیر اینصورت این ربات برای شما کار نخواهد کرد. سپس روی دکمه | <b>عضـو شـدم 🔐 | </b>"
            "کلیک کنید تا عضویت ربات خود را تأیید کنید."
        ),
        "verify_join": "عضـو شـدم 🔐",
        "join_channel_btn": "عضـو کانال ⚡",
        "not_joined": "🤨 شما عضو کانال ما نیستید. لطفاً عضو شوید و دوباره امتحان کنید.",
        "downloading": "<b>در حال دانلود، لطفاً صبر کنید</b> ...⏳🙃",
        "download_successful": "<b>دانلود با موفقیت انجام شد ✈️</b>",
        "error": "✗ متاسفانه مشکلی در دریافت اطلاعات پیش آمد 💔\nلطفا لینک را بررسی و دوباره امتحان کنید ⚡"
    }
}

# Check if user has joined the required channels
async def is_user_joined(user_id):
    for channel in Config.CHANNLS:
        try:
            member = await app.get_chat_member(channel, user_id)
            if member.status in ["kicked", "restricted", "left"]:
                return False
        except Exception:
            return False
    return True

# Function to process Instagram URL
async def fetch_instagram_media(client, message):
    url = message.text
    if "instagram.com" not in url:
        await message.reply_text(LANGUAGE_TEXTS["en"]["error"])
        return

    await message.reply_text(LANGUAGE_TEXTS["en"]["downloading"])

    try:
        response = requests.get(Config.API_BASE_URL + url)
        data = response.json()

        # Check for video or photo
        if data.get("video"):
            for video_url in data["video"]:
                await message.reply_video(video_url, caption=LANGUAGE_TEXTS["en"]["download_successful"])
        elif data.get("photo"):
            for photo_url in data["photo"]:
                await message.reply_photo(photo_url, caption=LANGUAGE_TEXTS["en"]["download_successful"])
        else:
            await message.reply_text(LANGUAGE_TEXTS["en"]["error"])
    except Exception as e:
        await message.reply_text(f"{LANGUAGE_TEXTS['en']['error']} {str(e)}")

# Welcome Message
@app.on_message(filters.private & filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    if not await is_user_joined(user_id):
        await message.reply_text(
            LANGUAGE_TEXTS["en"]["join_channel"],
            reply_markup=types.InlineKeyboardMarkup(
                [[types.InlineKeyboardButton(LANGUAGE_TEXTS["en"]["join_channel_btn"], url=f"https://t.me/{Config.CHANNLS[0]}")]]
            )
        )
        return

    await message.reply_text(LANGUAGE_TEXTS["en"]["welcome"])

# Instagram Media Downloader Handler
@app.on_message(filters.private & filters.text)
async def handle_instagram_url(client, message):
    await fetch_instagram_media(client, message)

# Run the bot
if __name__ == "__main__":
    app.run()
