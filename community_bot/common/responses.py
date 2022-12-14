from typing import Optional
import discord
class Notification(discord.Embed):
    TYPES = {
        "log" : { "color" : 0xFFFFFF, "icon" : "đ" }, 
        "info" : { "color" :  0x0080FF, "icon" : "âšī¸" },
        "important" : { "color" : 0xFFFF00, "icon" : "â ī¸" },
        "critical" : { "color" : 0xFF0000, "icon" : "đ¨" },
        "affirmative" : { "color" : 0x00FF80, "icon" : "â" },
    }
    
    def __init__(self, type: Optional[str] = "log", title: Optional[str] = None, content: Optional[str] = None, **kwargs):
        """Notification embeds for the bot
        Types:
            0: log đ (default)
            1: info âšī¸
            2: important â ī¸
            3: critical đ¨
            4: affirmative â
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
class ListEmbed(discord.Embed):
    EMOJIS = {
        0 : "0ī¸âŖ",
        1 : "1ī¸âŖ",
        2 : "2ī¸âŖ",
        3 : "3ī¸âŖ",
        4 : "4ī¸âŖ",
        5 : "5ī¸âŖ",
        6 : "6ī¸âŖ",
        7 : "7ī¸âŖ",
        8 : "8ī¸âŖ",
        9 : "9ī¸âŖ",
        10 : "đ",
    }
    
    def __init__(self, title: str, description: str, items: list, **kwargs):
        """Embed for listing items
        Args:
            title (str): Embed title
            description (str): Embed description
            items (list): List of items to list (max 11), format : [(field_name, field_value), ...]
        """
        assert len(items) <= len(self.EMOJIS), "Too many items to list"
        super().__init__(**kwargs)
        self.title = title
        self.description = description
        self.color = 0xFFFFFF
        for i, item in enumerate(items):
            self.add_field(name=f"{self.EMOJIS[i]} {item[0]}", value=item[1], inline=True)
            