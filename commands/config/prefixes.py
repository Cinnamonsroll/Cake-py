from discord.ext import commands
class Prefixes(commands.Cog):
    def __init__(self, client):
        self.client = client
        @commands.group(name="prefixes", description = "Add, remove and view prefixes", aliases=["prefix"])
        async def prefixes(self, ctx):
            if ctx.invoked_subcommand is None:
                await ctx.send("Please provide a valid subcommand either `add`, `delete` or `view`")
        @prefixes.command(name = "view", description = "View the servers prefixes", aliases = ["v"])
        async def view(self, ctx):
            print(self.client.cache["prefixes"][str(ctx.message.guild.id)])
def setup(client):
    client.add_cog(Prefixes(client))