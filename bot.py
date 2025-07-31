import discord
from discord.ext import commands, tasks
import asyncio
import os
import signal
import sys
from dotenv import load_dotenv
from scraper_playwright_async import get_news_with_browser
from utils import load_posted_links, save_posted_links

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

posted_links = load_posted_links()

@bot.event
async def on_ready():
    print(f"Conectado como {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} slash command(s) sincronizados")
    except Exception as e:
        print(f"Error al sincronizar commands: {e}")
    if not check_news.is_running():
        check_news.start()

@bot.tree.command(name="ping", description="Responde con Pong!")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!")

@bot.tree.command(name="force_news", description="[TEST] Fuerza la publicación de noticias nuevas")
async def force_news(interaction: discord.Interaction):
    await interaction.response.defer()
    try:
        news = await get_news_with_browser()
        new_items = [item for item in news if item[2] not in posted_links]

        if not new_items:
            await interaction.followup.send("No hay noticias nuevas para publicar")
            return

        channel = bot.get_channel(CHANNEL_ID)
        for title, description, link in new_items:
            message = f"{title}"
            if description:
                message += f"\n{description}"
            message += f"\nFuente: {link}"
            await channel.send(message)
            posted_links.add(link)

        save_posted_links(posted_links)
        await interaction.followup.send(f"{len(new_items)} noticia(s) publicada(s) manualmente")
    except Exception as e:
        await interaction.followup.send(f"Error al publicar noticias: {str(e)}")

@tasks.loop(minutes=30)
async def check_news():
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print(f"No se pudo encontrar el canal con ID: {CHANNEL_ID}")
        return

    try:
        news = await get_news_with_browser()
        new_items = [item for item in news if item[2] not in posted_links]

        if new_items:
            print(f"🔥 {len(new_items)} noticia(s) nueva(s) encontrada(s)")
            for title, description, link in new_items:
                message = f"{title}"
                if description:
                    message += f"\n{description}"
                message += f"\nFuente: {link}"
                await channel.send(message)
                posted_links.add(link)
            save_posted_links(posted_links)
        else:
            print("No hay noticias nuevas")
    except Exception as e:
        print(f"Error al obtener noticias: {e}")

@check_news.before_loop
async def before_check_news():
    await bot.wait_until_ready()

async def shutdown():
    print("🔄 Cerrando bot...")
    if check_news.is_running():
        check_news.cancel()
    await bot.change_presence(status=discord.Status.offline)
    save_posted_links(posted_links)
    await bot.close()
    print("Bot cerrado correctamente")

def signal_handler(signum, frame):
    print(f"\nSeñal {signum} recibida, cerrando bot...")
    asyncio.create_task(shutdown())

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

async def main():
    try:
        await bot.start(TOKEN)
    except KeyboardInterrupt:
        print("Interrupción por teclado detectada")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        if not bot.is_closed():
            await shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot terminado por el usuario")
    except Exception as e:
        print(f"Error fatal: {e}")
    finally:
        sys.exit(0)
