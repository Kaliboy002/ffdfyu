import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Your Telegram bot token
TELEGRAM_TOKEN = "8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM"  # Replace with your bot's token

# URL of the ChatGPT API
CHATGPT_API_URL = "https://api.smtv.uz/ai/?text="

# Function to handle user messages
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text  # Get the user's message

    # Send the message to the ChatGPT API
    response = requests.get(CHATGPT_API_URL + user_message)

    # Parse the JSON response
    response_data = response.json()

    # Extract the answer from the API response
    answer = response_data.get('answer', "Sorry, I couldn't understand that.")

    # Send the response back to the user
    await update.message.reply_text(answer)

# Function to start the bot
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! Send me a message, and I'll respond using ChatGPT.")

# Main function to set up the bot
def main():
    # Set up the Application with the bot's token
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add command handler for the start command
    application.add_handler(CommandHandler("start", start))

    # Add message handler for text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
