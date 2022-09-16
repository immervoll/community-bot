import typing
import discord
from discord.ext import commands
from discord import app_commands
from community_bot.common.responses import Notification

class GeneralCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(embed = Notification(custom_icon= "👋", custom_color=0xFFFFFFF, title = f"{member.name} joined", content=f'Welcome {member.mention} to the server 🥳.' ))

    @commands.hybrid_command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'Hello {member.name}')
        else:
            await ctx.send(f'Hello {member.name}... This feels familiar.')
        self._last_member = member
        self.bot.logger.info(f"{member.name} invoked the hello command")

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context, guilds: commands.Greedy[discord.Object] = None, spec: typing.Optional[typing.Literal["~", "*", "^"]] = None) -> None:
        """Syncs commands with Discord.
        Works like:
            !sync -> global sync
            !sync ~ -> sync current guild
            !sync * -> copies all global app commands to current guild and syncs
            !sync ^ -> clears all commands from the current guild target and syncs (removes guild commands)
            !sync id_1 id_2 -> syncs guilds with id 1 and 2

        Args:
            ctx (commands.Context): context of the command
            guilds (commands.Greedy[discord.Object]): list of guilds to sync
            spec (typing.Optional[typing.Literal[, optional): sync mode. Defaults to None.
        """
        try:
            if not guilds:
                if spec == "~":
                    synced = await ctx.bot.tree.sync(guild=ctx.guild)
                elif spec == "*":
                    ctx.bot.tree.copy_global_to(guild=ctx.guild)
                    synced = await ctx.bot.tree.sync(guild=ctx.guild)
                elif spec == "^":
                    ctx.bot.tree.clear_commands(guild=ctx.guild)
                    await ctx.bot.tree.sync(guild=ctx.guild)
                    synced = []
                else:
                    synced = await ctx.bot.tree.sync()
                await ctx.send(embed=Notification(custom_icon="🔁", custom_color=0x00FF00, title="Synced AppCommands", content=f"Synced {len(synced)} commands"), delete_after=5)
                return
            ret = 0
            for guild in guilds:
                try:
                    await ctx.bot.tree.sync(guild=guild)
                except discord.HTTPException:
                    pass
                else:
                    ret += 1
            await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")
        except discord.HTTPException as e:
            if e.status == 429:
                await ctx.send(embed=Notification(type=2, title="Rate Limited", content="You are being rate limited. Try again later."), delete_after=5)
    
        
async def setup(bot):
    await bot.add_cog(GeneralCog(bot))
