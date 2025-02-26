from constants.all_commands import (DEFAULT_COMMANDS, HABITS_COMMANDS,
                                    TRACKING_COMMANDS)

echo_message = "К сожалению я не знаю такой команды."
hello_message = "👋 Привет! Я бот для отслеживания привычек."

info_message = (
    "Привет! Я твой персональный помощник в формировании полезных привычек. "
    "Вместе мы будем следить за твоим прогрессом, "
    "помогать тебе не пропускать важные действия и достигать целей. "
    "Добавляй привычки, отмечай выполнение и следи "
    "за своими успехами — всё в одном месте! "
    "Начни сегодня, и завтра ты уже будешь на шаг ближе к своей лучшей версии!"
)


def create_command_descr_text_for_command_help(
    commands: tuple[tuple[str, str], ...],
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
