# bot.py
import discord
from discord.ext import commands, tasks
import asyncio
import os
import signal
import sys
from dotenv import load_dotenv
from scraper import get_latest_news
from utils import load_posted_links, save_posted_links

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# Usar commands.Bot en lugar de discord.Client para slash commands
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

posted_links = load_posted_links()

@bot.event
async def on_ready():
    print(f"✅ Conectado como {bot.user}")
    # Sincronizar slash commands
    try:
        synced = await bot.tree.sync()
        print(f"✅ {len(synced)} slash command(s) sincronizados")
    except Exception as e:
        print(f"❌ Error al sincronizar commands: {e}")
    
    # Iniciar el task de noticias
    if not check_news.is_running():
        check_news.start()

# Slash command /ping
@bot.tree.command(name="ping", description="Responde con Pong!")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!")

# Slash command para forzar publicación de noticias (solo para testing)
@bot.tree.command(name="force_news", description="[TEST] Fuerza la publicación de noticias nuevas")
async def force_news(interaction: discord.Interaction):
    await interaction.response.defer()
    
    try:
        latest_news = get_latest_news()
        new_items = [item for item in latest_news if item[1] not in posted_links]
        
        if not new_items:
            await interaction.followup.send("ℹ️ No hay noticias nuevas para publicar")
            return
        
        channel = bot.get_channel(CHANNEL_ID)
        published_count = 0
        
        for title, link in new_items:
            await channel.send(f"📰 **{title}**\n{link}")
            posted_links.add(link)
            published_count += 1
        
        save_posted_links(posted_links)
        await interaction.followup.send(f"✅ {published_count} noticia(s) publicada(s) manualmente")
        
    except Exception as e:
        await interaction.followup.send(f"❌ Error al publicar noticias: {str(e)}")

# Slash command para ver estadísticas
@bot.tree.command(name="stats", description="Muestra estadísticas del bot")
async def stats(interaction: discord.Interaction):
    try:
        latest_news = get_latest_news()
        total_news = len(latest_news) if latest_news else 0
        posted_count = len(posted_links)
        new_count = len([item for item in latest_news if item[1] not in posted_links]) if latest_news else 0
        
        # Calcular tiempo hasta próxima verificación
        if check_news.next_iteration:
            import datetime
            now = datetime.datetime.now(check_news.next_iteration.tzinfo)
            time_until_next = check_news.next_iteration - now
            
            if time_until_next.total_seconds() > 0:
                minutes_left = int(time_until_next.total_seconds() // 60)
                seconds_left = int(time_until_next.total_seconds() % 60)
                next_check_info = f"en {minutes_left}m {seconds_left}s"
            else:
                next_check_info = "pronto"
        else:
            next_check_info = "No programada"
        
        stats_text = f"""📊 **Estadísticas del Bot**
        
🔗 **Links ya publicados:** {posted_count}
📰 **Noticias en el sitio:** {total_news}
🆕 **Noticias nuevas disponibles:** {new_count}
⏰ **Próxima verificación:** {next_check_info}
🔄 **Task activo:** {'✅ Sí' if check_news.is_running() else '❌ No'}
⏱️ **Intervalo:** cada 30 minutos"""
        
        await interaction.response.send_message(stats_text)
        
    except Exception as e:
        await interaction.response.send_message(f"❌ Error al obtener estadísticas: {str(e)}")

@tasks.loop(minutes=30)  # Cada 30 minutos
async def check_news():
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print(f"❌ No se pudo encontrar el canal con ID: {CHANNEL_ID}")
        return

    try:
        latest_news = get_latest_news()
        new_items = [item for item in latest_news if item[1] not in posted_links]

        for title, link in new_items:
            await channel.send(f"📰 **{title}**\n{link}")
            posted_links.add(link)

        if new_items:
            save_posted_links(posted_links)
            print(f"✅ {len(new_items)} nueva(s) noticia(s) enviada(s)")
        else:
            print("ℹ️ No hay noticias nuevas")
            
    except Exception as e:
        print(f"❌ Error al obtener noticias: {e}")

@check_news.before_loop
async def before_check_news():
    await bot.wait_until_ready()

# Función para manejar el cierre del bot
async def shutdown():
    print("🔄 Cerrando bot...")
    
    # Detener el task de noticias
    if check_news.is_running():
        check_news.cancel()
    
    # Cambiar estado a offline antes de cerrar
    await bot.change_presence(status=discord.Status.offline)
    
    # Guardar links antes de cerrar
    save_posted_links(posted_links)
    
    # Cerrar la conexión
    await bot.close()
    print("✅ Bot cerrado correctamente")

# Manejar señales del sistema para cierre limpio
def signal_handler(signum, frame):
    print(f"\n🛑 Señal {signum} recibida, cerrando bot...")
    asyncio.create_task(shutdown())

# Registrar manejadores de señales
signal.signal(signal.SIGINT, signal_handler)   # Ctrl+C
signal.signal(signal.SIGTERM, signal_handler)  # Terminación del proceso

async def main():
    try:
        # Establecer estado como online al iniciar
        await bot.start(TOKEN)
    except KeyboardInterrupt:
        print("🛑 Interrupción por teclado detectada")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
    finally:
        # Asegurar cierre limpio
        if not bot.is_closed():
            await shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Bot terminado por el usuario")
    except Exception as e:
        print(f"❌ Error fatal: {e}")
    finally:
        sys.exit(0)