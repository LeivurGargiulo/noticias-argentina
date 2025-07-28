# Discord News Bot 🇦🇷

A Discord bot made in Python that automatically posts the latest news from [argentina.gob.ar/noticias](https://www.argentina.gob.ar/noticias).

## 🚀 How to use it

1. Clone the repo and navigate to the project:
   ```bash
   git clone https://github.com/your-username/discord-news-bot.git
   cd discord-news-bot
   ```

2. (Optional but recommended) Create a virtual environment:
   
   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   **macOS/Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file and add your Discord bot token and channel ID:
   ```env
   DISCORD_TOKEN=your_token_here
   CHANNEL_ID=your_channel_id_here
   ```

5. Run the bot:
   ```bash
   python bot.py
   ```

## 🧠 How it works
- Scrapes the official news website.
- Checks for updates every 30 minutes.
- Posts only new news using a local registry.

## 📦 Files
- `bot.py`: Main bot logic.
- `scraper.py`: Extracts news.
- `utils.py`: Loads and saves already posted URLs.
- `posted_news.json`: Logs posted URLs.
- `.env`: Stores your token and channel ID.
- `requirements.txt`: Project dependencies.
- `.gitignore`: Prevents sensitive files from being committed.

---

Created by Leivur ✨

> ⚠️ This project is not officially affiliated with the Government of Argentina.
