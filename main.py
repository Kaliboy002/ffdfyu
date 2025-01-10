import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Your bot's token
MASTER_BOT_TOKEN = "8179647576:AAEIsa7Z72eThWi-VZVW8Y7buH9ptWFh4QM"  # Replace with your bot's token

# Temporary storage for bot tokens
user_tokens = {}

# Start command handler
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Welcome to the Bot Maker!\n"
        "Send me a valid Telegram bot token, and I'll generate a ChatGPT bot script for you."
    )

# Function to handle received tokens
async def handle_token(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_message = update.message.text.strip()

    # Validate the provided token format
    if ":" not in user_message or not user_message.split(":")[0].isdigit():
        await update.message.reply_text("Invalid token format. Please send a valid Telegram bot token.")
        return

    # Save the user's token temporarily
    user_tokens[user_id] = user_message

    # Generate the bot script
    bot_script = generate_chatgpt_bot_script(user_message)

    # Save the bot script to a file
    file_path = f"ChatGPT_Bot_{user_id}.py"
    with open(file_path, "w") as bot_file:
        bot_file.write(bot_script)

    # Send the bot script back to the user
    await update.message.reply_text("Your ChatGPT bot script has been created! Download it below:")
    await context.bot.send_document(chat_id=update.message.chat_id, document=open(file_path, "rb"))

    # Clean up the generated file
    os.remove(file_path)

# Function to generate a ChatGPT bot script
def generate_chatgpt_bot_script(token):
    script = f"""
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Your bot's token
BOT_TOKEN = "{token}"  # Replace with your token

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
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command handler for the start command
    application.add_handler(CommandHandler("start", start))

    # Add message handler for text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
"""
    return script

# Main function to set up the bot
def main():
    # Set up the Application with the bot's token
    application = Application.builder().token(MASTER_BOT_TOKEN).build()

    # Add command handler for the start command
    application.add_handler(CommandHandler("start", start))

    # Add message handler for text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_token))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
