import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Your main bot's token
MAIN_BOT_TOKEN = "8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM"  # Replace with your main bot's token

# ChatGPT API URL
CHATGPT_API_URL = "https://api.smtv.uz/ai/?text="

# Temporary storage for user-provided tokens
user_tokens = {}

# Function to handle the /start command
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Welcome! I can help you create your own ChatGPT bot. Send me the token of the bot you'd like to power with ChatGPT!"
    )

# Function to handle user-provided tokens
async def handle_token(update: Update, context: CallbackContext):
    token = update.message.text.strip()

    # Validate the token using Telegram's getMe method
    response = requests.get(f"https://api.telegram.org/bot{token}/getMe")
    if response.status_code == 200:
        user_tokens[update.effective_user.id] = token
        await update.message.reply_text(
            "Great! Your token is valid. I'm now setting up your ChatGPT bot. Please wait..."
        )
        create_chatgpt_bot(token)
        await update.message.reply_text("Your ChatGPT bot is ready to use!")
    else:
        await update.message.reply_text("Invalid token. Please try again.")

# Function to create and deploy a ChatGPT bot
def create_chatgpt_bot(user_token):
    # Define the logic for the ChatGPT bot
    async def chatgpt_start(update: Update, context: CallbackContext):
        await update.message.reply_text("Hello! Send me a message, and I'll respond using ChatGPT.")

    async def chatgpt_handle_message(update: Update, context: CallbackContext):
        user_message = update.message.text
        response = requests.get(CHATGPT_API_URL + user_message)
        response_data = response.json()
        answer = response_data.get('answer', "Sorry, I couldn't understand that.")
        await update.message.reply_text(answer)

    # Create a new Application for the user's bot
    application = Application.builder().token(user_token).build()

    # Add handlers for the user's bot
    application.add_handler(CommandHandler("start", chatgpt_start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chatgpt_handle_message))

    # Run the user's bot in a separate thread
    application.run_polling()

# Main function to set up the main bot
def main():
    # Set up the Application for the main bot
    application = Application.builder().token(MAIN_BOT_TOKEN).build()

    # Add handlers for the main bot
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_token))

    # Run the main bot
    application.run_polling()

if __name__ == '__main__':
    main()
