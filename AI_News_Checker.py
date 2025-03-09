from google import genai
from typing import Final
from telegram import Update
from telegram.ext import Application , CommandHandler, MessageHandler, filters, ContextTypes

TOKEN :Final = 'telegram_api_token'
BOT_USERNAME: Final = 'bot_name'

GOOGLE_API_KEY: Final = "Google_API_Key"


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a fact checking bot \n Enter the link you want to verify")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "This is a fact checking bot which uses AI to check whether the link you have sent is factual or not")

# Message Handler
async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text
    response: str = get_ai_response(text)
    await update.message.reply_text(response)

# Error
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

def get_ai_response(link):
    client = genai.Client(api_key=GOOGLE_API_KEY)
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=f"Analyse the content of the article and tell me in one word real or fake, is this real or fake news?{link}"
    )
    print(response.text)
    return response.text


if __name__ == '__main__':
    print("Starting bot......")
    app = Application.builder().token(TOKEN).build()

    # Command
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_messages))

    # Error
    app.add_error_handler(error)

    print("Polling......")
    app.run_polling(poll_interval=3)