import discord
from discord.ext import commands,tasks
import requests

intents = discord.Intents.default()
intents.message_content = True
intents.presences = True

bot = commands.Bot(command_prefix='!',intents = intents)

def get_anime_recommendation():
    # Example response structure
    url = f"https://api.jikan.moe/v4/random/anime"
    res = requests.get(url)
    anime_data = res.json()
    anime_info = anime_data['data']
    title = anime_info['title']
    img = anime_info['images']['jpg']['image_url']
    link = anime_info['url']
    synopsis = anime_info['synopsis']
    score = anime_info['score']
    return {
        "title": title, 
        "score": score,
        "link": link,
        "synopsis": synopsis,
        "image url": img  # Assuming 'img' is defined earlier as the image URL
    }


@tasks.loop(minutes=1)
async def scheduled_recommendation():
    channel_id = 1220491031511040152  # Replace with your channel's ID
    channel = bot.get_channel(channel_id)
    if channel:
        anime = get_anime_recommendation()
        message = f"Today's anime recommendation is: **{anime['title']}** **{anime['score']}\n**\n{anime['synopsis']}\nMore info: {anime['link']}"
        await channel.send(message)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    scheduled_recommendation.start()


bot.run('MTIyMDQ2Mzg2NzUyNDU0NjYzMg.G9mySP.duNdXgH05l3Xic8vSPnoznJcwIstXjbnf8U748')  # Replace with your bot's token

