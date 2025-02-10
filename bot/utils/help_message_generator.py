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
