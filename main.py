import os
from PIL import Image
from telegram.ext import Updater, MessageHandler, Filters

def picture_to_sticker(bot, update):
    picture_file = bot.get_file(update.message.photo[-1].file_id)
    picture_file.download("picture.jpg")

    # Convert picture to sticker
    img = Image.open("picture.jpg")
    img.save("sticker.webp", "webp")

    sticker = open("sticker.webp", "rb")
    bot.send_sticker(chat_id=update.message.chat_id, sticker=sticker)

def main():
    # Get Telegram API key from environment
    API_KEY = os.environ["TELEGRAM_API_KEY"]

    # Set up Telegram bot
    updater = Updater(API_KEY)
    dp = updater.dispatcher

    # Add message handler
    dp.add_handler(MessageHandler(Filters.photo, picture_to_sticker))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
