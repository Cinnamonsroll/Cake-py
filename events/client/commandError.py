from discord.ext import commands
import re
class commandError(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(error)
        if re.search("Member(.*)not", str(error)):
            await ctx.send("Invalid member!")
def setup(client):
    client.add_cog(commandError(client))