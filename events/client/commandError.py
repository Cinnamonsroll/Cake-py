from discord.ext import commands
import re
class commandError(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(error)
        if re.search("Member(.*)not", str(error)):
            return await ctx.send("Invalid member!")
        elif re.search("You are missing(.*)permission", str(error)):
            return await ctx.send(str(error))
def setup(client):
    client.add_cog(commandError(client))