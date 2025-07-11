from decouple import config
from pytimeparse import parse
import ptbot
from functools import partial

TG_TOKEN = config('BOT_TOKEN')


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def reply(bot, seconds_left, chat_id, message_id, total_seconds):
    progress_bar = render_progressbar(
        total_seconds,
        total_seconds - seconds_left
    )
    bot.update_message(
        chat_id,
        message_id,
        f'Осталось: {seconds_left} секунд\n{progress_bar}'
    )


def finish_counting(bot, chat_id, original_message):
    bot.send_message(chat_id, 'Время вышло.')


def notify_progress(bot, author_id, message_text):
    total_seconds = parse(message_text)
    message_id = bot.send_message(author_id, 'Запускаю таймер')

    bot.create_countdown(
        total_seconds,
        partial(reply, bot),
        chat_id=author_id,
        message_id=message_id,
        total_seconds=total_seconds
    )

    bot.create_timer(
        total_seconds,
        partial(finish_counting, bot),
        chat_id=author_id,
        original_message=message_text
    )


def main():
    bot = ptbot.Bot(TG_TOKEN)
    bot.reply_on_message(partial(notify_progress, bot))
    bot.run_bot()

if __name__ == '__main__':
    main()
