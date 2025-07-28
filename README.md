# Discord News Bot 🇦🇷

Un bot de Discord hecho en Python que publica automáticamente las últimas noticias de [argentina.gob.ar/noticias](https://www.argentina.gob.ar/noticias).

## 🚀 Cómo usarlo

1. Cloná el repo y navegá al proyecto.
2. Instalá las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Copiá el archivo `.env.example` como `.env` y agregá tu token de Discord y el ID del canal.
4. Ejecutá el bot:
   ```bash
   python bot.py
   ```

## 🧠 Cómo funciona
- Scrapea la web oficial de noticias.
- Verifica cada 30 minutos si hay novedades.
- Publica solo noticias nuevas usando un registro local.

## 📦 Archivos
- `bot.py`: Lógica principal del bot.
- `scraper.py`: Extrae las noticias.
- `utils.py`: Carga y guarda las URLs ya posteadas.
- `.env`: Configuración secreta.
- `posted_news.json`: Registro de URLs posteadas.

---

Creado por Leivur ✨

> Nota: Este proyecto no está afiliado oficialmente al Gobierno de Argentina.
"# noticias-argentina" 
