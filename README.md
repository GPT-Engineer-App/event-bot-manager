# Telegram Board Game Bot

## Setup

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/telegram-board-game-bot.git
   cd telegram-board-game-bot
   ```

2. Create a `.env` file with your Telegram bot token:

   ```sh
   echo "TELEGRAM_BOT_TOKEN=your-telegram-bot-token" > .env
   ```

3. Build and run the Docker containers:

   ```sh
   docker-compose up --build
   ```

4. Initialize the database:
   ```sh
   docker-compose exec bot python -c "from database import init_db; init_db()"
   ```

## Usage

- `/start` - Start the bot
- `/help` - Show help
- `/newevent` - Create a new event
- `/newgame` - Add a new game
- `/show_games` - Show all games
- `/my_like_games` - Show favorite games
