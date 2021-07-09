import discord
from discord.ext import commands
class Tags(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(name="tags", description="View, list, create, update, or delete a server tag", aliases=["t", "tag"])
    @commands.guild_only()
    async def tags(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Please provide a valid subcommand either `add`, `delete`, `edit`, `alias`, or `use`")

    @tags.command(name="use", description="Use a tag", aliases=["u"])
    async def use(self, ctx, tag=None):
        guildData = self.client._guilds.find_one(
            {"guild": str(ctx.guild.id)})
        if tag == None or not len(list(filter(lambda x: x["name"] == tag or tag in x["aliases"], guildData["tags"]))) > 0:
            return await ctx.send("Tag not found")
        else:
            foundTag = list(
                filter(lambda x: x["name"] == tag or tag in x["aliases"], guildData["tags"]))[0]
            return await ctx.send(foundTag["content"])
    @tags.command(name="view", description="View all tags", aliases=["list"])
    async def view(self, ctx):
        guildData = self.client._guilds.find_one(
            {"guild": str(ctx.guild.id)})
        if len(guildData["tags"]) <= 0:
            return await ctx.send("This server has no tags")
        tags = [guildData["tags"][i:i+10]
                for i in range(0, len(guildData["tags"]), 10)]
        embeds = []
        for tag in tags:
            embed = discord.Embed(color=self.client.color, title="Tags",
                                  description=f"{', '.join(['`' + x['name'] + '`' for x in tag])}")
            embeds.append(embed)
        await self.client.pagination(self.client, ctx, ctx.message, embeds)

    @tags.command(name="delete", description="Deletes a tag", aliases=["remove"])
    @commands.has_permissions(manage_messages=True)
    async def add(self, ctx, name=None):
        guildData = self.client._guilds.find_one(
            {"guild": str(ctx.guild.id)})
        if not name:
            return await ctx.send("Please include a valid name")
        if len(list(filter(lambda x: x["name"] == name, guildData["tags"]))) <= 0:
            return await ctx.send("Tag doesn't exist")
        foundTag = list(
            filter(lambda x: x["name"] == name, guildData["tags"]))[0]
        if not foundTag["owner"] == ctx.message.author.id:
            return await ctx.send("You do not own this tag")
        guildData["tags"] = list(
            filter(lambda x: not x["name"] == name, guildData["tags"]))
        self.client._guilds.find_one_and_update(
            {"guild": str(ctx.guild.id)}, {"$set": guildData})
        return await ctx.send("Tag deleted")

    @tags.command(name="edit", description="Edits a tag", aliases=["update"])
    @commands.has_permissions(manage_messages=True)
    async def edit(self, ctx, name=None, *, content=None):
        guildData = self.client._guilds.find_one(
            {"guild": str(ctx.guild.id)})
        if not name or not content:
            return await ctx.send("Please include a valid name and content")
        if len(list(filter(lambda x: x["name"] == name, guildData["tags"]))) <= 0:
            return await ctx.send("Tag doesn't exist")
        foundTag = list(
            filter(lambda x: x["name"] == name, guildData["tags"]))[0]
        if not foundTag["owner"] == ctx.message.author.id:
            return await ctx.send("You do not own this tag")
        guildData["tags"][next((index for (index, d) in enumerate(
            guildData["tags"]) if d["name"] == name), None)]["content"] = content
        self.client._guilds.find_one_and_update(
            {"guild": str(ctx.guild.id)}, {"$set": guildData})
        return await ctx.send("Tag edited")
    @tags.command(name="add", description="Adds a tag", aliases=["create"])
    @commands.has_permissions(manage_messages=True)
    async def add(self, ctx, name=None, *, content=None):
        guildData = self.client._guilds.find_one(
            {"guild": str(ctx.guild.id)})
        if not name or not content:
            return await ctx.send("Please include a valid name and content")
        if len(list(filter(lambda x: x["name"] == name or name in x["aliases"], guildData["tags"]))) > 0 or name in ["create", "add", "use", "u", "view", "list", "delete", "remove", "edit", "update", "alias", "meta", "info"]:
            return await ctx.send("Tag already exists or restricted name")
        guildData["tags"].append(
            {"name": name, "content": content, "owner": ctx.message.author.id, "aliases": []})
        self.client._guilds.find_one_and_update(
            {"guild": str(ctx.guild.id)}, {"$set": guildData})
        return await ctx.send("Tag created")
    @tags.command(name="alias", description="Add an alias to a tag")
    @commands.has_permissions(manage_messages=True)
    async def alias(self, ctx, name=None, alias=None):
        guildData = self.client._guilds.find_one(
            {"guild": str(ctx.guild.id)})
        if not name or not alias:
            return await ctx.send("Please include a valid name and alias")
        if len(list(filter(lambda x: x["name"] == name, guildData["tags"]))) <= 0:
            return await ctx.send("Tag doesn't exist")
        foundTag = list(
            filter(lambda x: x["name"] == name, guildData["tags"]))[0]
        if not foundTag["owner"] == ctx.message.author.id:
            return await ctx.send("You do not own this tag")
        guildData["tags"][next((index for (index, d) in enumerate(
            guildData["tags"]) if d["name"] == name), None)]["aliases"].append(alias)
        self.client._guilds.find_one_and_update(
            {"guild": str(ctx.guild.id)}, {"$set": guildData})
        return await ctx.send("Alias added")
    @tags.command(name="meta", description="Get info on a tag", aliases=["tag"])
    async def meta(self, ctx, name=None):
        guildData = self.client._guilds.find_one(
            {"guild": str(ctx.guild.id)})
        if not name:
            return await ctx.send("Please include a valid name and alias")
        if len(list(filter(lambda x: x["name"] == name or name in x["aliases"], guildData["tags"]))) <= 0:
            return await ctx.send("Tag doesn't exist")
        foundTag = list(
            filter(lambda x: x["name"] == name or name in x["aliases"], guildData["tags"]))[0]
        return await ctx.send(f"Name: {foundTag['name']}\nContent: {foundTag['content']}\nAliases: {'None' if len(foundTag['aliases']) <= 0 else ', '.join(foundTag['aliases'])}\nOwner: {self.client.get_user(foundTag['owner'])}")
def setup(client):
    client.add_cog(Tags(client))