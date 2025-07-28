# Discord News Bot 🇦🇷

A Discord bot made in Python that automatically posts the latest news from [argentina.gob.ar/noticias](https://www.argentina.gob.ar/noticias).

## 🚀 How to use it

1. Clone the repo and navigate to the project.
2. Install the dependencies:
```bash
pip install -r requirements.txt
```
3. Copy the `.env.example` file as `.env` and add your Discord token and channel ID.
4. Run the bot:
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

---

Created by Leivur ✨
