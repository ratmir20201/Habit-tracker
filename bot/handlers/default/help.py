from bot.main import tg_bot
from handlers.constants.all_commands import ALL_COMMANDS


@tg_bot.message_handler(commands=["help"])
def help_message(message):
    commands = [
        "/{command} - {description}".format(
            command=command,
            description=description,
        )
        for command, description in ALL_COMMANDS
    ]
    print(commands)
    tg_bot.reply_to(message, "\n".join(commands))
