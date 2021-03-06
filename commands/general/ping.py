from discord.ext import commands
class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.command(name="ping", aliases=["pong"], description="Gets bot latency")
    @commands.guild_only()
    async def ping(self, ctx):
        await ctx.send(f"Pong! `{round(self.client.latency * 1000)}`ms")
      

def setup(client):
    client.add_cog(Ping(client))