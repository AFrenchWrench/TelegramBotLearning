from typing import Final

from telegram import (
    Update,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineQueryResultPhoto,
)
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    InlineQueryHandler,
)

from omdb_client import search_movie_by_title

BOT_TOKEN: Final = "BOT_TOKEN"


async def start_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello, I'm a bot! Thanks for using me!",
        reply_to_message_id=update.effective_message.id,
    )


async def search_movie_inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    elif "only_poster" in query:
        query = query.replace("only_poster", "")
        query = query.strip()
        movies = search_movie_by_title(query)
        results = [
            InlineQueryResultPhoto(
                id=m.imdb_id,
                caption=f"{m.title} - {m.year}",
                title=m.title,
                thumbnail_url=m.poster,
                photo_url=m.poster,
            )
            for m in movies
        ]
        await context.bot.answer_inline_query(update.inline_query.id, results)
    else:
        movies = search_movie_by_title(query)
        results = [
            InlineQueryResultArticle(
                id=m.imdb_id,
                title=m.title,
                input_message_content=InputTextMessageContent(
                    message_text=f"{m.title} - {m.year}:\n\nhttps://www.imdb.com/title/{m.imdb_id}/"
                ),
                thumbnail_url=m.poster,
            )
            for m in movies
        ]
        await context.bot.answer_inline_query(update.inline_query.id, results)


if __name__ == "__main__":
    bot = ApplicationBuilder().token(BOT_TOKEN).build()

    # adding handlers
    bot.add_handler(CommandHandler("start", start_command_handler))
    bot.add_handler(InlineQueryHandler(search_movie_inline_query))

    # start bot
    bot.run_polling()
