# bot.py
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackQueryHandler
from database import SessionLocal, init_db
from models import User, Game, Event
from sqlalchemy.orm import sessionmaker

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Initialize the database
init_db()

# Define the start command handler
def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    session = SessionLocal()
    db_user = session.query(User).filter(User.telegram_id == user.id).first()
    if not db_user:
        db_user = User(telegram_id=user.id, username=user.username)
        session.add(db_user)
        session.commit()
    update.message.reply_text(f"👋 Hello, {user.first_name}! Welcome to the Board Game Bot. Use /help to see available commands.")

# Define the help command handler
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Available commands:\n/start - Start the bot\n/help - Show help\n/newevent - Create a new event\n/newgame - Add a new game\n/show_games - Show all games\n/my_like_games - Show favorite games")

# Define the new event command handler
def newevent(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Creating a new event...")

# Define the new game command handler
def newgame(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Adding a new game...")

# Define the show games command handler
def show_games(update: Update, context: CallbackContext) -> None:
    session = SessionLocal()
    games = session.query(Game).all()
    if games:
        games_list = "\n".join([f"{game.name} - {game.description}" for game in games])
        update.message.reply_text(f"Available games:\n{games_list}")
    else:
        update.message.reply_text("No games available.")

# Define the my like games command handler
def my_like_games(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    session = SessionLocal()
    db_user = session.query(User).filter(User.telegram_id == user.id).first()
    if db_user and db_user.favorite_games:
        favorite_games_list = "\n".join([game.name for game in db_user.favorite_games])
        update.message.reply_text(f"Your favorite games:\n{favorite_games_list}")
    else:
        update.message.reply_text("You have no favorite games.")

def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater("YOUR_TELEGRAM_BOT_TOKEN")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("newevent", newevent))
    dispatcher.add_handler(CommandHandler("newgame", newgame))
    dispatcher.add_handler(CommandHandler("show_games", show_games))
    dispatcher.add_handler(CommandHandler("my_like_games", my_like_games))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()