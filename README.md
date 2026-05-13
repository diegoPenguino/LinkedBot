# Telegram LinkedIn Post Manager

An AI-powered Telegram bot designed to help you capture your daily professional activities and transform them into engaging LinkedIn posts. Built with **FastAPI**, **aiogram**, **SQLAlchemy**, and **OpenAI**.

## 🚀 Features
- **Instant Capture**: Send any thought or activity to the bot, and it automatically extracts a title and summary.
- **Smart Drafting**: Generate professional LinkedIn posts using OpenAI, tailored to your personal professional context.
- **Media Advice**: Get recommendations on how many pictures or what kind of media to pair with your post.
- **Persistent Tracking**: Manage a numbered list of pending posts and mark them as completed once posted.

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/diegoPenguino/LinkedBot
   cd LinkedBot
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # Linux/macOS:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

Create a `.env` file in the root directory (you can use `.env.example` as a template):

```env
TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
OPENAI_API_KEY="your_openai_api_key"
PERSONAL_CONTEXT="A brief description of who you are, what you do, and your writing style."
```

> [!IMPORTANT]
> You **must** provide both the Telegram Bot Token (from @BotFather) and your OpenAI API Key for the project to function.

## 🏃 Running the Application

Start the FastAPI server and the Telegram bot:

```bash
python main.py
```

The bot will start in long-polling mode, and the FastAPI server will be available at `http://localhost:8000`.

## 🤖 Bot Commands
- `/start`: Initial welcome and help message.
- `/list`: Display all pending posts.
- `/draft <id>`: Generate a LinkedIn post draft for the specific item.
- `/done <id>`: Mark a post as completed.
- *Any text*: Simply send any message to add a new activity to your pending list.

## ⚖️ License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
