from telegram import Update, InlineKeyboardButton, BotCommand, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters


class TelegramBot:

    def __init__(self, token: str) -> None:
        self.app = ApplicationBuilder().token(token).build()
        self.register_handlers()
        # TODO: реализовать отдельный json-файл который будет
        #  хранить все данные user_data и чтобы при инициализации и
        #  начале чата он брал эти данные оттуда и при надобности
        #  удалял, перезаписывал отдельными методами и манипулировал

    # Helping method to create an inline-keyboard with one or multiple line buttons
    @staticmethod
    def _keyboard_creator(keyboard_format: str, keyboard_data: list[tuple[str, str]] |
                          list[list[tuple[str, str]]]) -> InlineKeyboardMarkup:
        if not keyboard_data:
            raise ValueError("Keyboard must contain at least 1 button")

        fmt = keyboard_format.strip().lower()
        if fmt == "multiline":
            rows = [
                [InlineKeyboardButton(text, callback_data=data) for text, data in row] for row in keyboard_data
            ]
            return InlineKeyboardMarkup(rows)

        elif fmt == "oneline":
            buttons = [
                [InlineKeyboardButton(text, callback_data=data) for text, data in keyboard_data]
            ]
            return InlineKeyboardMarkup(buttons)

    # Method to register all handlers
    def register_handlers(self) -> None:
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("help", self.help))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.state_handler))

    # Structured method to encapsulate different scenarios for handlers
    async def state_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> any:
        if context.user_data.get("waiting_name"):
            return await self._general_info(update, context)
        elif context.user_data.get("waiting_new_exercise"):
            return await self._add_exercise(update, context)

    # Method which response to /start command and return info of
    # chosen exercise block depends on which user has chosen
    @staticmethod
    async def _general_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        response = update.message.text
        if response == "🔴Block A":
            # TODO: create a json file with all exercises
            block_a_exercises = "Push-ups, ..."
            await update.message.reply_text(block_a_exercises)
        elif response == "🔵Block B":
            block_b_exercises = "Squats, ..."
            await update.message.reply_text(block_b_exercises)
        context.user_data.pop("waiting_name")

    @staticmethod
    async def _add_exercise(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:



    # Method to greet user and launch the main menu for choice
    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        context.user_data["waiting_name"] = True
        keyboard = [["🔴Block A", "🔵Block B"]]
        markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        await update.message.reply_text("No time for rest!\n Keep grinding!🦾", reply_markup=markup)

    @staticmethod
    async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await context.bot.set_my_commands([
            BotCommand("start", "Welcome user and send main buttons to choose block"),
            BotCommand("help", "Return list of all available commands")
        ])
        command_list = await context.bot.get_my_commands()
        my_commands = "\n".join(f"/{command.command} - {command_list.description}" for command in command_list)
        await update.message.reply_text(f"All available commands:\n{my_commands}")

    @staticmethod
    async def add_exercise(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        context.user_data["waiting_new_exercise"] = True
        await context.message.reply_text("Enter the name, category and description of exercise"
                                         " which you would like to add. Use newline character as a delimiter")




