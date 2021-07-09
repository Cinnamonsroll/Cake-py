  
from discord.ext import commands

async def prefixes(client, message):
    if message.guild:
        if not "prefixes" in client.cache: client.cache["prefixes"] = {}
        if str(message.guild.id) in client.cache["prefixes"]:
            return commands.when_mentioned_or(*client.cache["prefixes"][str(message.guild.id)])(client, message)
        else:
            guild = client._guilds.find_one({"guild": str(message.guild.id)})
            if guild == None: 
                guild = client._guilds.insert_one({"guild": str(message.guild.id), "prefixes": ["c~"], "tags": []})
                guild = client._guilds.find_one({"guild": str(message.guild.id)})
            client.cache["prefixes"][str(message.guild.id)] = guild["prefixes"]
            return commands.when_mentioned_or(*client.cache["prefixes"][str(message.guild.id)])(client, message)
    else: 
        return commands.when_mentioned_or(*["c~"])(client, message)
        