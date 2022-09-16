import json
import typing
import discord
from discord.ext import commands
from discord import app_commands
from community_bot.common.responses import Notification

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
        else:
            channel = channel.resolve()
            
        message = await channel.send(embed = Notification(0, "Event", "This is a dummy event"))
        self.events.update({event_id : message.id})
          
        await interaction.response.send_message(embed=Notification(type=4, title="Event posted", content=f"Successfully posted {event_id}"), ephemeral=True)
        
    @events.command(name="update")
    async def update(self, interaction: discord.Interaction, message_id: str) -> None:
        message = await interaction.channel.fetch_message(int(message_id))
        await message.edit(embed = Notification(custom_icon = "👷‍♂️", custom_color=0xFFFF00, title="Updated Event", content="This is an updated dummy event"))
        await interaction.response.send_message(embed=Notification(type="affirmative", title="Event Updated", content=f"Successfully updated {message_id}"), ephemeral=True)
    
    @events.command(name="list")
    async def list(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(embed=Notification(title="Event List", content=f"Here is a list with all Events:\n1. Placeholder\n2. Placeholder"), ephemeral=True)
    
    
    
    slots = app_commands.Group(name="slot", description="...")
    
    @slots.command(name="join")
    async def join(self, interaction: discord.Interaction, event_id: int, slot_id: int) -> None:
          
        await interaction.response.send_message(embed=Notification("affirmative","Joined Slot",f"Successfully joined slot {slot_id} for event {event_id}"), ephemeral=True)
        
    @slots.command(name="leave")
    async def leave(self, interaction: discord.Interaction, event_id: int, slot_id: int) -> None:
          
        await interaction.response.send_message(embed=Notification(1,"Left Slot" ,f"Left slot {slot_id} for event {event_id}"), ephemeral=True)
        
    
    @slots.command(name="forcejoin")
    @commands.has_guild_permissions(administrator=True)
    async def forcejoin(self, interaction: discord.Interaction, event_id: int, slot_id: int, user: discord.User) -> None:
          
        await interaction.response.send_message(embed=Notification(2, "Force Join", f"{user.mention} joined slot {slot_id} for event {event_id} forcefully"), ephemeral=True)
    
    @slots.command(name="forceleave")
    @commands.has_guild_permissions(administrator=True)
    async def forceleave(self, interaction: discord.Interaction, event_id: int, slot_id: int, user: discord.User) -> None:
        
        await interaction.response.send_message(embed= Notification(2, "Force leave", f"{user.mention} left slot {slot_id} for event {event_id} forcefully"), ephemeral=True)
    
    
        
async def setup(bot):
    await bot.add_cog(EventsCog(bot))
