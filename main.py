from abc import ABC
import fivempy
import discord
from discord.ext import commands
from discord.ext import tasks
import requests
import random
import chat_exporter
import io


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
        await interaction.response.send_message(f"Please wait...", ephemeral=True)
        channel = await guild.create_text_channel(name=f"ticket-{interaction.user.id}", overwrites=overwrites)
        await interaction.channel.send(f"{channel.mention}")
        await channel.send("Close ticket... (only an Admin can close a ticket)", view=CloseTicket())


class CloseTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.red, emoji="🎟️", custom_id="btn2")
    async def button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        admin_id = "admin role id here"
        debug_channel = bot.get_channel("debug_channel id here")
        for i in interaction.user.roles:
            if i.id == admin_id:
                await interaction.response.send_message(f"Closing ticket. Please wait...", ephemeral=True)
                await archive(interaction.channel, debug_channel)
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
        embed = discord.Embed(title="SERVER NAME HERE", color=discord.Color.green())
        channel = bot.get_channel("CHANNEL ID HERE")
        msg = await channel.send(embed=embed)
        get_server_info.start(msg)
        server = fivempy.Server("SERVER IP HERE")
        activity = discord.Game(
            name=f"🎮 PlayersOnline - {server.get_player_count()}/48 | 🌏 IpAddress - SERVER IP HERE",
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
guild_ids = [1062999855590543360]


@tasks.loop(seconds=1)
async def get_server_info(embed):
    msg = embed
    embed = discord.Embed(color=discord.Color.green(), title="SERVER NAME HERE")
    try:
        requests.get(url="http://SERVER IP HERE", timeout=5)
        status = "🟢 - Online!"
    except requests.exceptions.RequestException:
        status = "❌ - Offline!"
    server = fivempy.Server("SERVER IP HERE")
    embed.add_field(name="📊 - IsOnline:", value=status)
    embed.add_field(name="🌏 - IP Address:", value="```SERVER IP HERE```")
    await msg.edit(embed=embed)


@bot.event
async def on_member_join(member: discord.Member):
    guild = bot.get_guild("GUILD ID HERE)
    start_role = guild.get_role("ROLE ID HERE")
    welcome_channel = bot.get_channel("WELCOME CHANNEL ID HERE")
    await member.edit(roles=[start_role])
    await welcome_channel.send(f"{random.choice(greetings)}, {member.mention}! "
                               f"The entire team wishes you to have a GOOD TIME!")


@bot.event
async def on_member_remove(member: discord.Member):
    leave_channel = bot.get_channel("LEAVE CHANNEL ID HERE")
    await leave_channel.send(f"{member.name} left us. :cry:")


@bot.slash_command(name="list", description="Returns the players currently playing in the server.", guild_ids=guild_ids)
async def player_list(ctx: discord.ApplicationContext):
    server = fivempy.Server("SERVER IP HERE")
    player_string = [f"{i}\n" for i in server.get_player_list()]
    main_str = ''.join(player_string)
    print(main_str)
    await ctx.respond("Player list:")
    await ctx.send(f"```{main_str}```")


@bot.slash_command(name="create_button", guild_ids=guild_ids)
async def button(ctx):
    await ctx.respond("Ok.")
    await ctx.send("You have a question? You're at the right place.", view=OpenTicket())


<<<<<<< HEAD
async def archive(channel, archive_channel):
    if channel and archive_channel:
        transcript = await chat_exporter.export(channel)
        transcript_file = discord.File(io.BytesIO(transcript.encode()), filename=f"{channel.name}.html")

        await archive_channel.send(file=transcript_file)


bot.run('MTA2MjgzMDUyMDk5MzU5NTQ0Mg.G0tODx.zxq_5vrcDAP4-aWdYk-Yq7cUmt0HEJ-yUsjvXw')
=======
bot.run('YOUR TOKEN HERE')
>>>>>>> 5081a7a02b7ac70390060527a059ac3b531a18ab
