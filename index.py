import discord
from discord.ext.commands import Bot
import json
import os
from functions.pagination import pagination
from functions.prefixes import prefixes
import pymongo
f = open("config.json")
data = json.load(f)
mongoConnection = pymongo.MongoClient(data["mongo"])

intents = discord.Intents.default()
client = Bot(command_prefix=prefixes, intents=intents, case_insensitive = True)
client.owner_ids = data["owners"]
client.remove_command("help")
client._botData = mongoConnection["cakepy"]
client._guilds = client._botData["guilds"]
client.cache = {}
client.pagination = pagination
client.color = int(hex(int("FFFEFB", 16)), 0)
for folder in os.listdir('./commands'):
    for file in os.listdir(f"./commands/{folder}"):
        if file.endswith('.py'):
            print(f"Loading command {file[:-3]}")
            client.load_extension(f"commands.{folder}.{file[:-3]}")
for folder in os.listdir('./events'):
    for file in os.listdir(f"./events/{folder}"):
        if file.endswith('.py'):
            print(f"Loading event {file[:-3]}")
            client.load_extension(f"events.{folder}.{file[:-3]}")
client.run(data["token"])