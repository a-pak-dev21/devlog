from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ApplicationBuilder, CommandHandler, MessageHandler, filters


class TelegramBotPractice:

    def __init__(self, token: str) -> None:
        self.app = ApplicationBuilder().token(token).build()
        self.register_handlers()

    def run(self) -> None:
        self.app.run_polling()

    def register_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("help", self.help))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.echo))
        self.app.add_handler(CommandHandler("about", self.about))
        self.app.add_handler(CommandHandler("say", self.say, has_args=True))

    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Hello, I'm bot! How can i help you?")

    @staticmethod
    async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        all_commands = await context.bot.get_my_commands()
        cmd_list = "\n".join(f"/{cmd.command} - {cmd.description}"for cmd in all_commands)
        await update.message.reply_text(f"All available commands:\n{cmd_list}")

    @staticmethod
    async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.message.text.strip().lower() == "hello":
            await update.message.reply_text(f"Hello {update.effective_user.name}!")
        else:
            await update.message.reply_text(update.message.text)

    @staticmethod
    async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("I'm training bot, which made to practice Telegram module")

    @staticmethod
    async def say(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(f"You said: {' '.join(context.args)}")

    @staticmethod
    async def choose():
        pass



