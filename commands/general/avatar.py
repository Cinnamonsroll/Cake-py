from discord.ext import commands
import discord
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
def createSizes(member, extension):
  sizes = [128, 256, 512, 1024, 2048, 4096]
  string = []
  for size in sizes:
    string.append(f"[{size}x]({member.avatar_url_as(format=(extension), size=size)})")
  return " | ".join(string)
class Avatar(commands.Cog):
    def __init__(self, client,):
        self.client = client
    @commands.command(name="avatar", aliases=["pfp"], description="Get a user's avatar")
    @commands.guild_only()
    async def avatar(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.message.author
        avatar = str(member.avatar_url_as(format=("gif" if member.is_avatar_animated() else "png")))
        extensions = ["png", "jpeg", "jpg", "webp", "gif"] if avatar.find("gif") != -1 else [ "png", "jpeg", "jpg", "webp"]
        avatarEmbeds = []
        for extension in extensions:
            embed = discord.Embed(color=self.client.color,title=f"`{member.name}\'s` avatar", description=f"`{extension.upper()}` {createSizes(member, extension)}")
            embed.set_image(url=member.avatar_url_as(format=(extension), size=2048))
            avatarEmbeds.append(embed)
        await self.client.pagination(self.client, ctx, ctx.message, avatarEmbeds)
def setup(client):
    client.add_cog(Avatar(client))