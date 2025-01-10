import requests
from telegram import Update, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import logging

# Enable logging for better debugging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Your Telegram bot token
TELEGRAM_TOKEN = "8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM"  # Replace with your bot's token

# URL of the ChatGPT API
CHATGPT_API_URL = "https://api.smtv.uz/ai/?text="

# Welcome Image and Description
WELCOME_IMAGE_URL = "https://example.com/welcome_image.jpg"  # Replace with actual image URL
WELCOME_DESCRIPTION = "Welcome to the ChatGPT-powered bot! Ask me anything and I'll try to help you."

# Function to handle user messages
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text  # Get the user's message

    try:
        # Send the message to the ChatGPT API
        response = requests.get(CHATGPT_API_URL + user_message, timeout=10)

        # Check if the response was successful
        if response.status_code == 200:
            response_data = response.json()
            answer = response_data.get('answer', "Sorry, I couldn't understand that.")
        else:
            answer = "Sorry, there was an issue with the API. Please try again later."

    except requests.exceptions.RequestException as e:
        logger.error(f"API Request failed: {e}")
        answer = "Sorry, I couldn't connect to the API. Please try again later."

    # Send the response back to the user
    await update.message.reply_text(answer)

# Function to send the welcome message with an image when the bot is started
async def start(update: Update, context: CallbackContext):
    await update.message.reply_photo(WELCOME_IMAGE_URL, caption=WELCOME_DESCRIPTION)
    await update.message.reply_text("Hello! Send me a message, and I'll respond using ChatGPT.")

# Function to send the help message explaining the bot usage
async def help(update: Update, context: CallbackContext):
    help_message = (
        "Here are some commands you can use:\n"
        "/start - Get a welcome message and start interacting with the bot\n"
        "/help - View this help message\n"
        "Just type a question or message, and I'll answer using ChatGPT.\n"
        "Example: 'What is AI?'"
    )
    await update.message.reply_text(help_message)

# Function to send additional information about the bot
async def info(update: Update, context: CallbackContext):
    info_message = (
        "This bot is powered by ChatGPT, an AI model that answers your questions.\n"
        "The bot uses a custom API that connects to ChatGPT.\n"
        "Developed by: @BestProger"
    )
    await update.message.reply_text(info_message)

# Main function to set up the bot
def main():
    # Set up the Application with the bot's token
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add command handler for the start command
    application.add_handler(CommandHandler("start", start))

    # Add command handler for the help command
    application.add_handler(CommandHandler("help", help))

    # Add command handler for the info command
    application.add_handler(CommandHandler("info", info))

    # Add message handler for text messages (excluding commands)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
