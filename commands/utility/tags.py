from discord.ext import commands
import discord
class Tags(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.group(name="tags", description = "View, list, create, update, or delete a server tag", aliases=["t", "tag"])
    @commands.guild_only()
    async def tags(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Please provide a valid subcommand either `add`, `delete`, `rename`, `edit`, `alias`, or `use`")
    @tags.command(name="use", description="Use a tag", aliases=["u"])
    async def use(self, ctx, tag = None):
        guildData = self.client._guilds.find_one({"guild": str(ctx.message.guild.id)})
        if tag == None or not len(list(filter(lambda x: x["name"] == tag, guildData["tags"]))) > 0:
            return await ctx.send("Tag not found")
        else: 
            foundTag = list(filter(lambda x: x["name"] == tag, guildData["tags"]))[0]
            return await ctx.send(foundTag["content"])
    @tags.command(name="add", description="Add a tag", aliases=["create"])
    @commands.has_permissions(manage_messages = True)
    async def add(self, ctx, name = None, content = None):
        guildData = self.client._guilds.find_one({"guild": str(ctx.message.guild.id)})
        if not name or not content:
            return await ctx.send("Please include a valid name and content")
        if len(list(filter(lambda x: x["name"] == name, guildData["tags"]))) > 0 or name in ["create", "add", "use", "u"]:
            return await ctx.send("Tag already exists or restricted name")
        guildData["tags"].append({"name": name, "content": content, "owner": ctx.message.author.id, "aliases": []})
        self.client._guilds.find_one_and_update({"guild": str(ctx.message.guild.id)}, {"$set": guildData})
        return await ctx.send("Tag created")
def setup(client):
    client.add_cog(Tags(client))