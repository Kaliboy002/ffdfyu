import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Your Telegram bot token
TELEGRAM_TOKEN = "8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM"  # Replace whith your bot's token

# URL of the ChatGPT API
CHATGPT_API_URL = "https://api.smtv.uz/ai/?text="

# Function to handle user messages
def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text  # Get the user's message

    # Send the message to the ChatGPT API
    response = requests.get(CHATGPT_API_URL + user_message)

    # Parse the JSON response
    response_data = response.json()

    # Extract the answer from the API response
    answer = response_data.get('answer', "Sorry, I couldn't understand that.")

    # Send the response back to the user
    update.message.reply_text(answer)

# Function to start the bot
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! Send me a message, and I'll respond using ChatGPT.")

# Main function to set up the bot
def main():
    # Set up the Updater with the bot's token
    updater = Updater(TELEGRAM_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add command handler for the start command
    dispatcher.add_handler(CommandHandler("start", start))

    # Add message handler for text messages
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the bot
    updater.start_polling()

    # Run the bot until you send a signal to stop it
    updater.idle()

if __name__ == '__main__':
    main()
