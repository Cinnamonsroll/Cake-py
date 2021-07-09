from discord.ext import commands
import discord
class Prefixes(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.group(name="prefixes", description = "Add, remove and view prefixes", aliases=["prefix"])
    @commands.guild_only()
    async def prefixes(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Please provide a valid subcommand either `add`, `delete` or `view`")
    @prefixes.command(name="view", description="View the servers prefixes", aliases=["v"])
    async def view(self, ctx):
        prefixes = self.client.cache["prefixes"][str(ctx.message.guild.id)]
        formattedPrefixes = [f"{prefixes.index(x) + 1}. {x}" for x in prefixes]
        embed = discord.Embed(color=self.client.color, title="Showing prefixes", description='\n'.join(formattedPrefixes))
        await ctx.send(embed=embed)
    @prefixes.command(name="add", description="Add a server prefix", aliases=["create"])
    @commands.has_permissions(manage_messages = True)
    async def add(self, ctx, *, prefix = None):
        prefixes = self.client.cache["prefixes"][str(ctx.message.guild.id)]
        guildData = self.client._guilds.find_one({"guild": str(ctx.message.guild.id)})
        if prefix == None:
            return await ctx.send("Please include a valid prefix")
        if prefix in prefixes:
            return await ctx.send("This prefix already exists")
        guildData["prefixes"].append(prefix)
        self.client._guilds.find_one_and_update({"guild": str(ctx.message.guild.id)}, {"$set": guildData})
        self.client.cache["prefixes"][str(ctx.message.guild.id)] = self.client._guilds.find_one({"guild": str(ctx.message.guild.id)})["prefixes"]
        await ctx.send("Prefix added!")
    @prefixes.command(name="remove", description="Remove a server prefix", aliases=["delete"])
    @commands.has_permissions(manage_messages = True)
    async def add(self, ctx, *, prefix = None):
        prefixes = self.client.cache["prefixes"][str(ctx.message.guild.id)]
        guildData = self.client._guilds.find_one({"guild": str(ctx.message.guild.id)})
        if prefix == None:
            return await ctx.send("Please include a valid prefix")
        if not prefix in prefixes:
            return await ctx.send("This prefix does not exist")
        if len(prefixes) == 1:
            return await ctx.send("You must have atleast one prefix")
        guildData["prefixes"] = list(filter(lambda x: not x == prefix, guildData["prefixes"]))
        self.client._guilds.find_one_and_update({"guild": str(ctx.message.guild.id)}, {"$set": guildData})
        self.client.cache["prefixes"][str(ctx.message.guild.id)] = self.client._guilds.find_one({"guild": str(ctx.message.guild.id)})["prefixes"]
        await ctx.send("Prefix removed!")
        
def setup(client):
    client.add_cog(Prefixes(client))