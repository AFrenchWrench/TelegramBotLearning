from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    filters,
    MessageHandler,
)
from decouple import config
import logging

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("bot.log"),  # Logs to a file named 'bot.log'
        logging.StreamHandler(),  # Also logs to the console
    ],
)

# Set logging level for specific libraries
logging.getLogger("httpx").setLevel(logging.WARNING)

# Get the logger instance
logger = logging.getLogger(__name__)


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Received /start command from %s", update.effective_user.username)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"Hi {update.effective_user.username}!"
    )


async def echo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Echoing message: %s", update.message.text)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text
    )


async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    logger.info("Alarm triggered for chat_id %s with data %s", job.chat_id, job.data)
    await context.bot.send_message(
        job.chat_id, text=f"Beep! {job.data} seconds are over!"
    )


async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_message.chat_id
    try:
        due = float(context.args[0])
        if due < 0:
            raise ValueError("Negative time not allowed")
    except (IndexError, ValueError):
        logger.error("Invalid time provided by user.")
        await context.bot.send_message(
            chat_id,
            text=f"Invalid time. Please provide a positive number. e.g., /set 5",
        )
        return

    logger.info("Setting timer for %s seconds", due)
    context.job_queue.run_once(alarm, due, chat_id=chat_id, name=str(chat_id), data=due)


if __name__ == "__main__":
    application = ApplicationBuilder().token(config("APItoken")).build()

    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("set", set_timer))

    # Message Handler
    application.add_handler(MessageHandler(filters.TEXT, echo_handler))

    logger.info("Bot is starting...")
    application.run_polling()
