from discord.ext import commands
from discord_components import DiscordComponents
class Ready(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        DiscordComponents(self.client)
        print('Ready!')
def setup(client):
    client.add_cog(Ready(client))