from typing import Final

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
)

BOT_TOKEN: Final = "BOT_TOKEN"


async def start_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello, I'm a bot! Thanks for using me!",
        reply_to_message_id=update.effective_message.id,
    )


async def add_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    a, b = int(context.args[0]), int(context.args[1])
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"{a} + {b} = {a+b}",
        reply_to_message_id=update.effective_message.id,
    )


async def multiplication_command_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    a, b = int(context.args[0]), int(context.args[1])
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"{a} * {b} = {a * b}",
        reply_to_message_id=update.effective_message.id,
    )


async def calculate_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    exp = " ".join(context.args)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"{exp} = {eval(exp)}",
        reply_to_message_id=update.effective_message.id,
    )


if __name__ == "__main__":
    bot = ApplicationBuilder().token(BOT_TOKEN).build()

    bot.add_handler(CommandHandler("start", start_command_handler))
    bot.add_handler(CommandHandler("add", add_command_handler))
    bot.add_handler(CommandHandler("mult", multiplication_command_handler))
    bot.add_handler(CommandHandler("calc", calculate_command_handler))

    # start bot
    bot.run_polling()
