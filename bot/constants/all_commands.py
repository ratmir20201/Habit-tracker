DEFAULT_COMMANDS = (
    ("hello", "👋 Приветствие."),
    ("help", "ℹ️ Показать список команд."),
    ("info", "ℹ️ Получить информацию о боте."),
    ("start", "🚀 Запустить бота."),
    ("login", "🔑 Войти в аккаунт."),
    ("logout", "🚪 Выйти из аккаунта."),
    # Команда имеется, но не рекомендуется к показу
    # ("register", "Зарегистрировать нового пользователя."),
)

HABITS_COMMANDS = (
    ("gethabits", "📋 Получить список своих привычек."),
    ("addhabit", "➕ Добавить новую привычку."),
    ("edithabit", "✏️ Изменить название привычки."),
    ("deletehabit", "🗑️ Удалить привычку."),
)

TRACKING_COMMANDS = (
    ("trackone", "Пометить определенную привычку как выполненную."),
    ("trackall", "Отправляет список привычек с кнопками ✅ и ❌."),
)

ALL_COMMANDS = DEFAULT_COMMANDS + HABITS_COMMANDS + TRACKING_COMMANDS
