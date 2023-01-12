from abc import ABC
import fivempy
import discord
from discord.ext import commands
from discord.ext import tasks
import requests
import random


class OpenTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.green, emoji="🎟️", custom_id="btn1")
    async def button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        guild = bot.get_guild("your guild id here")
        member = interaction.user
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True)
        }

        channel = await guild.create_text_channel(name=f"ticket-{interaction.user.id}", overwrites=overwrites)
        await channel.send("Close ticket... (only an Admin can close a ticket)", view=CloseTicket())
        await interaction.response.send_message(f"Opening ticket... {channel.mention}", ephemeral=True)


class CloseTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.red, emoji="🎟️", custom_id="btn2")
    async def button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        admin_id = "your admin role id"
        for i in interaction.user.roles:
            if i.id == admin_id:
                await interaction.channel.delete()
                return
        await interaction.response.send_message("❌ You don't have permissions to do that! ❌")


class PersistentViewBot(commands.Bot, ABC):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(
            command_prefix=commands.when_mentioned_or("/"), intents=intents
        )
        self.persistent_views_added = False

    async def on_ready(self):
        await self.wait_until_ready()
        embed = discord.Embed(title="YOUR SERVER NAME HERE", color=discord.Color.green())
        channel = bot.get_channel("STATUS CHANNEL ID HERE")
        msg = await channel.send(embed=embed)
        get_server_info.start(msg)
        server = fivempy.Server("5M SERVER IP ADDRESS HERE")
        activity = discord.Game(
            name=f"🎮 PlayersOnline - {server.get_player_count()}/48 | 🌏 IpAddress - 5M SERVER IP ADDRESS HERE",
            type=3)
        await bot.change_presence(activity=activity)
        if not self.persistent_views_added:
            self.add_view(OpenTicket())
            self.add_view(CloseTicket())
            self.persistent_views_added = True

        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")


bot = PersistentViewBot()

greetings = ["Welcome", "Here he comes", "Hop on", "We've got some work to do", "Greetings", "Come in"]
guild_ids = ["GUILD ID HERE"]


@tasks.loop(seconds=1)
async def get_server_info(embed):
    msg = embed
    embed = discord.Embed(color=discord.Color.green(), title="YOUR SERVER NAME HERE")
    try:
        requests.get(url="http://5M SERVER IP ADDRESS HERE", timeout=5)
        status = "🟢 - Online!"
    except requests.exceptions.RequestException:
        status = "❌ - Offline!"
    server = fivempy.Server("5M SERVER IP ADDRESS HERE")
    embed.add_field(name="📊 - IsOnline:", value=status)
    embed.add_field(name="🌏 - IP Address:", value="```5M SERVER IP ADDRESS HERE```")
    await msg.edit(embed=embed)

<<<<<<< HEAD

@bot.event
async def on_member_join(member: discord.Member):
    guild = bot.get_guild("guild id here")
    start_role = guild.get_role("start role id here")
    welcome_channel = bot.get_channel("join channel id here")
    await member.edit(roles=[start_role])
    await welcome_channel.send(f"{random.choice(greetings)}, {member.mention}! "
                               f"The entire team wishes you to have a GOOD TIME!")


@bot.event
async def on_member_remove(member: discord.Member):
    leave_channel = bot.get_channel("leave channel id here{")
    await leave_channel.send(f"{member.name} left us. :cry:")


@bot.slash_command(name="list", description="Returns the players currently playing in the server.", guild_ids=guild_ids)
async def player_list(ctx: discord.ApplicationContext):
    server = fivempy.Server("5M IP ADDRESS HERE")
    player_string = [f"{i}\n" for i in server.get_player_list()]
    main_str = ''.join(player_string)
    print(main_str)
    await ctx.respond("Player list:")
    await ctx.send(f"```{main_str}```")


@bot.slash_command(name="create_button", guild_ids=guild_ids)
async def button(ctx):
    await ctx.respond("Ok.")
    await ctx.send("You have a question? You're at the right place.", view=OpenTicket())


bot.run('YOUR TOKEN HERE')
=======
bot.run('YourTokenHere')
>>>>>>> aec8d9e064e992cac9db8e09fe7f107c011c2a62
