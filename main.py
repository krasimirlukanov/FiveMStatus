import fivempy
import discord
from discord.ext import tasks
import requests

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
    print("Started!")
    await bot.wait_until_ready()
    embed = discord.Embed(title="YOUR SERVER NAME", color=discord.Color.green())
    channel = bot.get_channel(the id of the channel where you want to send the message)
    msg = await channel.send(embed=embed)
    get_server_info.start(msg)
    server = fivempy.Server("YOUR IP HERE")
    activity = discord.Game(name=f"🎮 PlayersOnline - {server.get_player_count()}/48 | 🌏 IpAddress - YOUR IP HERE",
                            type=3)
    await bot.change_presence(activity=activity)


@tasks.loop(seconds=1)
async def get_server_info(embed):
    msg = embed
    embed = discord.Embed(color=discord.Color.green(), title="YOUR SERVER NAME")
    try:
        requests.get(url="http://YOUR IP HERE", timeout=5)
        status = "🟢 - Online!"
    except requests.exceptions.RequestException:
        status = "❌ - Offline!"
    server = fivempy.Server("YOUR IP HERE")
    embed.add_field(name="📊 - IsOnline:", value=status)
    embed.add_field(name="🌏 - IP Address:", value="```YOUR IP HERE```")
    player_string = [f"```{i}```\n" for i in server.get_player_list()]
    embed.add_field(name=f"🧑🏻‍🤝‍🧑🏾 - Players Online: {server.get_player_count()}/48",
                    value=''.join(player_string))
    embed.set_thumbnail(url="you can put an logo if you like, if not delete this line")
    embed.set_footer(text="here you can put some text if you like")
    await msg.edit(embed=embed)

bot.run('YourTokenHere')
