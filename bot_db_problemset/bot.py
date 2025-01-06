from typing import Any, Final

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
)
from telegram.ext._application import Application
from telegram.ext._callbackcontext import CallbackContext
from telegram.ext._extbot import ExtBot
from telegram.ext._jobqueue import JobQueue

from mongo_client import ExpenseMongoClient

BOT_TOKEN: Final = "7211398124:AAHCrwTsYKsweDV3_tQs-qj5M44V0PN7FlI"
# connect to your mongodb
db_client = ExpenseMongoClient("localhost", 27017)


async def start_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello, I'm a bot! Thanks for using me!",
        reply_to_message_id=update.effective_message.id,
    )


async def add_expense_command_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    db_client.add_expense(
        user_id=int(update.effective_user.id),
        amount=int(context.args[0]),
        category=context.args[1],
        description=" ".join(context.args[2:]),
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Expense added successfully!",
        reply_to_message_id=update.effective_message.id,
    )


def parse_expense(expense):
    txt = []
    for e in expense:
        txt.append(f"{e['amount']} - {e['category']} - {e['description']}")
    return "\n".join(txt)


async def get_expenses_command_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    if not context.args:
        expense = db_client.get_expenses(user_id=int(update.effective_user.id))
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Your expenses are:\n" + parse_expense(expense),
            reply_to_message_id=update.effective_message.id,
        )
    else:
        expense = db_client.get_expenses_by_category(
            user_id=int(update.effective_user.id), category=context.args[0]
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Your expenses are:\n" + parse_expense(expense),
            reply_to_message_id=update.effective_message.id,
        )


async def get_categories_command_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    categories = db_client.get_categories(user_id=int(update.effective_user.id))
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Your categories are: " + ", ".join(categories),
        reply_to_message_id=update.effective_message.id,
    )


async def get_total_expense_command_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    expense = db_client.get_total_expense(user_id=int(update.effective_user.id))
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Your total expense is: {expense}",
        reply_to_message_id=update.effective_message.id,
    )


async def get_total_expense_by_category_command_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    expense = db_client.get_total_expense_by_category(
        user_id=int(update.effective_user.id)
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Your total expense by category is:\n"
        + "\n".join([f"{k}: {v}" for k, v in expense.items()]),
        reply_to_message_id=update.effective_message.id,
    )


if __name__ == "__main__":
    expense_mongo_client = ExpenseMongoClient("localhost", 27017)
    bot: Application[
        ExtBot[None],
        CallbackContext[ExtBot[None], dict[Any, Any], dict[Any, Any], dict[Any, Any]],
        dict[Any, Any],
        dict[Any, Any],
        dict[Any, Any],
        JobQueue[
            CallbackContext[
                ExtBot[None], dict[Any, Any], dict[Any, Any], dict[Any, Any]
            ]
        ],
    ] = (
        ApplicationBuilder().token(BOT_TOKEN).build()
    )

    # adding handlers
    bot.add_handler(CommandHandler("start", start_command_handler))
    bot.add_handler(CommandHandler("add_expense", add_expense_command_handler))
    bot.add_handler(CommandHandler("get_expenses", get_expenses_command_handler))
    bot.add_handler(CommandHandler("get_categories", get_categories_command_handler))
    bot.add_handler(CommandHandler("get_total", get_total_expense_command_handler))
    bot.add_handler(
        CommandHandler(
            "get_total_by_category",
            get_total_expense_by_category_command_handler,
        )
    )

    # start bot
    bot.run_polling()
