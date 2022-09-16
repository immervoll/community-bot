import json
import typing
import discord
from discord.ext import commands
from discord import app_commands

class EventsCog(commands.Cog):
    events : dict
    def __init__(self, bot):
        self.bot = bot
        self.events = {}
        super().__init__()
        

    events = app_commands.Group(name="event", description="...")
    
    @events.command(name="post")
    async def post(self, interaction: discord.Interaction, event_id: int = None, channel: typing.Optional[discord.app_commands.AppCommandChannel] = None) -> None:
        
        if event_id is None:
            event_id = 0
            # get newest event
            pass
        
        if channel is None:
            channel = interaction.channel
        
        message = await channel.send(f"👷‍♂️ Event {event_id} Dummy")
        self.events.update({event_id : message.id})
          
        await interaction.response.send_message(f"Posted event {event_id} in {channel.mention}", ephemeral=True)
        
    @events.command(name="update")
    async def update(self, interaction: discord.Interaction, message_id: str) -> None:
        message = await interaction.channel.fetch_message(int(message_id))
        await message.edit(content="👷‍♂️ Event 1 Dummy - Updated")
        await interaction.response.send_message(f"✅ Updated Event", ephemeral=True)
    
    @events.command(name="list")
    async def list(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(f"📝 Event List", ephemeral=True)
    
    
    
    slots = app_commands.Group(name="slot", description="...")
    
    @slots.command(name="join")
    async def join(self, interaction: discord.Interaction, event_id: int, slot_id: int) -> None:
          
        await interaction.response.send_message(f"✅ Joined slot {slot_id} for event {event_id}", ephemeral=True)
        
    @slots.command(name="leave")
    async def leave(self, interaction: discord.Interaction, event_id: int, slot_id: int) -> None:
          
        await interaction.response.send_message(f"✅ Left slot {slot_id} for event {event_id}", ephemeral=True)
        
    
    @slots.command(name="forcejoin")
    @commands.has_guild_permissions(administrator=True)
    async def forcejoin(self, interaction: discord.Interaction, event_id: int, slot_id: int, user: discord.User) -> None:
          
        await interaction.response.send_message(f"✅ {user.mention} joined slot {slot_id} for event {event_id}", ephemeral=True)
    
    @slots.command(name="forceleave")
    @commands.has_guild_permissions(administrator=True)
    async def forceleave(self, interaction: discord.Interaction, event_id: int, slot_id: int, user: discord.User) -> None:
        
        await interaction.response.send_message(f"✅ {user.mention} left slot {slot_id} for event {event_id}", ephemeral=True)
    
    
        
async def setup(bot):
    await bot.add_cog(EventsCog(bot))