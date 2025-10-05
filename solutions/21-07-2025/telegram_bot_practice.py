from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler


class TelegramBotPractice:

    def __init__(self, token: str) -> None:
        self.app = ApplicationBuilder().token(token).build()
        self.register_handlers()

    def run(self) -> None:
        self.app.run_polling()

    def register_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("help", self.help))
        self.app.add_handler(CommandHandler("choice", self.choice))
        self.app.add_handler(CallbackQueryHandler(self.handle_inline_button))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_reply_button))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.message_handler))
        self.app.add_handler(CommandHandler("about", self.about))
        self.app.add_handler(CommandHandler("say", self.say, has_args=True))
        self.app.add_handler(CommandHandler("choose", self.choose))
        self.app.add_handler(CommandHandler("game", self.game))
        self.app.add_handler(CommandHandler("menu", self.menu))
        self.app.add_handler(CommandHandler("register", self.register))
        self.app.add_handler(CommandHandler("survey", self.survey))
        self.app.add_handler(CommandHandler("quest", self.quest))

    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Hello, I'm bot! How can i help you?")

    @staticmethod
    async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        all_commands = await context.bot.get_my_commands()
        cmd_list = "\n".join(f"/{cmd.command} - {cmd.description}"for cmd in all_commands)
        await update.message.reply_text(f"All available commands:\n{cmd_list}")

    @staticmethod
    async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        respond = update.message.text.strip()
        if context.user_data.get("awaiting_name"):
            context.user_data["name"] = respond.capitalize()
            context.user_data.pop("awaiting_name")

        elif context.user_data["survey_stage"] == 1:
            context.user_data["survey"]["color"] = respond
            context.user_data["survey_stage"] = 2
            await update.message.reply_text("Question 2: What's your favorite animal?")

        elif context.user_data["survey_stage"] == 2:
            context.user_data["survey"]["animal"] = respond
            context.user_data["survey_stage"] = 3
            await update.message.reply_text("Question 3: What's your dream job?")

        elif context.user_data["survey_stage"] == 3:
            context.user_data["survey"]["job"] = respond
            context.user_data.pop("survey_stage")

            summary = context.user_data["survey"]
            await update.message.reply_text(
                f"🌈 Favorite color: {summary['color']}\n"
                f"🐾 Favorite animal: {summary['animal']}\n"
                f"💼 Dream job: {summary['job']}"
            )

        elif respond.lower() == "hello":
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
    async def choose(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        keyboard = [["Who are you?", "What can you do?"]]
        markup = ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
        await update.message.reply_text("Choose: ", reply_markup=markup)

    @staticmethod
    async def handle_reply_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        response = update.message.text.strip()
        if response == "Who are you?":
            await update.message.reply_text("I'm GymNote Bot! Nice to meet you")
        elif response == "What can you do?":
            await update.message.reply_text("I can do planty different things!")

    @staticmethod
    async def choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        keyboard = [
            [InlineKeyboardButton("Yes", callback_data="yes")],
            [InlineKeyboardButton("No", callback_data="no")]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Choose one from following options: ", reply_markup=markup)

    @staticmethod
    async def game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        keyboard = [
            [InlineKeyboardButton("🧙 Mage", callback_data="role_mage"),
             InlineKeyboardButton("⚔️ Warrior", callback_data="role_warrior"),
             InlineKeyboardButton("🏹 Ranger", callback_data="role_ranger")]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("What would you like to do?\n", reply_markup=markup)

    @staticmethod
    async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        keyboard = [
            [InlineKeyboardButton("Attack", callback_data="attack"),
             InlineKeyboardButton("Check Stats", callback_data="check_stats"),
             InlineKeyboardButton("Back", callback_data="back")]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.message.reply_text("What would you like to do?\n", reply_markup=markup)

    @staticmethod
    async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        context.user_data["awaiting_name"] = True
        await update.message.reply_text("What is your name, adventurer?")

    @staticmethod
    async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        profile = (f"🧝Name: {context.user_data['name']}\n⚔️Class {context.user_data['class']}\n"
                   f"❤️HP: {context.user_data['stats']['HP']}\n🔮Mana: {context.user_data['stats']['Mana']}")
        await update.message.reply_text(profile)

    @staticmethod
    async def survey(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        context.user_data["survey_stage"] = 1
        context.user_data["survey"] = {}
        await update.message.reply_text("Question 1: What's your favorite color?")

    @staticmethod
    async def quest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        keyboard = [
            [
                InlineKeyboardButton("🏔️Mountains", callback_data="mountain_road"),
                InlineKeyboardButton("🌲Forest", callback_data="forest_road"),
                InlineKeyboardButton("🏘️Village", callback_data="village_road")
            ]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Fork road ahead, choose the path:\n", reply_markup=markup)

    async def handle_inline_button(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()
        answer = query.data
        if answer == "yes":
            await query.edit_message_text(f"You've chosen: Yes")
        elif answer == "no":
            await query.edit_message_text(f"You've chosen: No")

        elif answer == "role_mage" or answer == "role_warrior" or answer == "role_ranger":
            context.user_data["stats"] = {"HP": 100, "Mana": 50}
            role = answer.replace("role_","").capitalize()
            context.user_data["class"] = role
            await query.edit_message_text(f"You chose: {role}")
            await self.menu(update, context)

        elif answer == "attack":
            await query.edit_message_text("You attack the enemy!")
        elif answer == "check_stats":
            stats_list = [f"{key}: {val}" for key,val in context.user_data["stats"].items()]
            await query.edit_message_text(f"Your stats:\n{'\n'.join(stats_list)}")
        elif answer == "back":
            context.user_data["role"] = None
            await self.game(update, context)

        elif answer.endswith("_road"):
            context.user_data["route"] = [answer.replace("_road", "")]
            keyboard = [
                [
                    InlineKeyboardButton("Left", callback_data="turn_left"),
                    InlineKeyboardButton("Right", callback_data="turn_right")
                ]
            ]
            markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("Choose where to turn?\n", reply_markup=markup)

        elif answer.startswith("turn_"):
            context.user_data["route"].append(answer.replace("turn_", "path_to_"))
            route = " -> ".join(elem.capitalize() for elem in context.user_data["route"])
            context.user_data.pop("route")
            #context.user_data["final_path"] = True
            await query.edit_message_text(f"Your final route is {route}")


my_token = "8049335645:AAHjB-HM0NsXc2p_HD3LA0qOz07TszjmTHI"
new_bot = TelegramBotPractice(my_token)
new_bot.run()
