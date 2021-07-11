from discord.ext import commands
import os
import discord
class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.command(name="help", aliases=["h"], description="Help command")
    @commands.guild_only()
    async def help(self, ctx, command=None):
        Command = None if command == None else self.client.get_command(command)
        if Command == None or not Command:
            categories = {}
            for folder in os.listdir('./commands'):
                if not folder in categories: categories[folder] = []
                for file in os.listdir(f"./commands/{folder}"):
                    if file.endswith('.py'):
                        categories[folder].append(file[:-3])
            formattedData = [f"**{category.title()}**\n{', '.join(commands)}" for category, commands in categories.items()]
            embed = discord.Embed(color=self.client.color, title="Help command", description="\n".join(formattedData))
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=self.client.color, title=f"{Command.name}", description=f"Description: {Command.description}\nAliases: {', '.join(Command.aliases)}")
            await ctx.send(embed=embed)
def setup(client):
    client.add_cog(Help(client))