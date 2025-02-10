from constants.all_commands import DEFAULT_COMMANDS, HABITS_COMMANDS, TRACKING_COMMANDS
from telebot.types import Message

from bot.main import tg_bot
from utils.help_message_generator import create_command_descr_text_for_command_help


@tg_bot.message_handler(commands=["help"])
def help_message(message: Message):
    message_text = "*Стандартные команды:*\n"
    default_commands = create_command_descr_text_for_command_help(DEFAULT_COMMANDS)
    message_text += default_commands

    message_text += "\n\n*Команды для взаимодействия с привычками:*\n"
    habits_commands = create_command_descr_text_for_command_help(HABITS_COMMANDS)
    message_text += habits_commands

    message_text += "\n\n*Команды для трекинга привычек:*\n"
    tracking_commands = create_command_descr_text_for_command_help(TRACKING_COMMANDS)
    message_text += tracking_commands

    tg_bot.send_message(message.chat.id, message_text, parse_mode="Markdown")
