from constants.all_commands import (DEFAULT_COMMANDS, HABITS_COMMANDS,
                                    TRACKING_COMMANDS)

echo_message = "К сожалению я не знаю такой команды."
hello_message = "👋 Привет! Я бот для отслеживания привычек."

info_message = (
    "Я помогу вам выработать новые хорошие привычки. Мы будем вместе отслеживать ваши действия и замерять ваш прогресс. "
    "Помните лучшее время чтобы начать это сегодня."
)


def create_command_descr_text_for_command_help(
    commands: tuple[tuple[str, str]],
) -> str:
    text_commands = "\n".join(
        "/{command} - _{description}_".format(
            command=command,
            description=description,
        )
        for command, description in commands
    )

    return text_commands


def generate_help_message() -> str:
    message_text = "*Стандартные команды:*\n"
    default_commands = create_command_descr_text_for_command_help(DEFAULT_COMMANDS)
    message_text += default_commands

    message_text += "\n\n*Команды для взаимодействия с привычками:*\n"
    habits_commands = create_command_descr_text_for_command_help(HABITS_COMMANDS)
    message_text += habits_commands

    message_text += "\n\n*Команды для трекинга привычек:*\n"
    tracking_commands = create_command_descr_text_for_command_help(TRACKING_COMMANDS)
    message_text += tracking_commands

    return message_text
