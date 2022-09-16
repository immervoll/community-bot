from typing import Optional
import discord
class Notification(discord.Embed):
    TYPES = {
        "log" : { "color" : 0xFFFFFF, "icon" : "📝" }, 
        "info" : { "color" :  0x0080FF, "icon" : "ℹ️" },
        "important" : { "color" : 0xFFFF00, "icon" : "⚠️" },
        "critical" : { "color" : 0xFF0000, "icon" : "🚨" },
        "affirmative" : { "color" : 0x00FF80, "icon" : "✅" },
    }
    
    def __init__(self, *, type: Optional[str] = "log", title: Optional[str] = None, content: Optional[str] = None, **kwargs):
        """Notification embeds for the bot
        Types:
            0: log 📝 (default)
            1: info ℹ️
            2: important ⚠️
            3: critical 🚨
            4: affirmative ✅
        Args:
            type (Optional[str], optional): Notification Type. Defaults to "log".
            title (Optional[str], optional): Notification Title. Defaults to None.
            content (Optional[str], optional): Notification Content. Defaults to None.
            *Note: Tho title and content are optional, both of them must be provided.
        Keyword Args:
            custom_color (discord.Color, optional): Custom color for the embed.
            custom_icon (str, optional): Custom icon for the embed.
            *Note: If you use custom_color or custom_icon, the type argument will be ignored. Both have to be used together.
        """        
        assert type in self.TYPES or int(type) in range(len(self.TYPES)), f"Invalid notification type: {type}"
        assert title and content, "Notification must have a title and content"
        
        if type not in self.TYPES:
            type = list(self.TYPES.keys())[int(type)]
            
        super().__init__(**kwargs)
        if not kwargs.get("custom_icon") and not kwargs.get("custom_color"):
            self.color = self.TYPES[type]["color"]
            self.add_field(name=f"{self.TYPES[type]['icon']} {title}", value=content, inline=False)
        if kwargs.get("custom_icon") and kwargs.get("custom_color"): 
            assert kwargs.get("custom_icon") and kwargs.get("custom_color"), "Custom icon and color must both be provided"
            self.color = kwargs.get("custom_color")
            self.add_field(name=f"""{kwargs.get("custom_icon")} {title}""", value=content, inline=False)