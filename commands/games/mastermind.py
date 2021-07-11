from discord.ext import commands
import discord
import random
class MasterMind(commands.Cog):
    def __init__(self, client,):
        self.client = client
    @commands.command(name="mastermind", aliases=["mm"], description="Play a game of mastermind against the bot",)
    @commands.guild_only()
    async def mastermind(self, ctx):
        emojis = ["🟦", "🟥", "🟪", "🟨", "🟩", "🟧"]
        gameEmojis = [*emojis, "⬅️", "✅"]
        gameGoing = True
        userGuesses = []
        def makeCode(length):
            code = []
            while len(code) < length:
                randomPick = random.choice(emojis)
                if not randomPick in code: code.append(randomPick)
            return code
        code = makeCode(4)
        lives = 10
        gameMessage = await ctx.send(f"Lives: {lives}\nYour guess:{''.join(userGuesses[0]) if len(userGuesses) > 0 else ''}")
        for emoji in gameEmojis:
            await gameMessage.add_reaction(emoji)
        print(code)
        while gameGoing:
            game = await self.client.wait_for("raw_reaction_add", check = lambda x: x.message_id == gameMessage.id and str(x.emoji) in gameEmojis and x.member.id == ctx.message.author.id)
            if str(game.emoji) == "✅":
                rightSpot = 0
                wrongSpot = 0
                for i in range(4):
                    if userGuesses[0]["guesses"][i] == code[i]: rightSpot += 1
                    if userGuesses[0]["guesses"][i] in code[i]: wrongSpot += 1
                lives -= 1
                userGuesses[0]["rightEmojis"] = list(f"{'🔁' * wrongSpot} {'✅' * rightSpot}")
                formattedGuesses = '\n'.join(f"{''.join(x['guesses'])} {''.join(filter(lambda y: y, x['rightEmojis']))}" for x in userGuesses[1:])
                if lives == 0:
                    gameGoing = False
                    return await gameMessage.edit(f"You lost\nLives: {lives}\nYour guess:\n\n{formattedGuesses if len(userGuesses) >= 1 else ''}")
                await gameMessage.edit(f"{'You won!' if rightSpot == 4 else ''}\nLives: {lives}\nYour guess:\n\n{formattedGuesses if len(userGuesses) >= 1 else ''}")
                if rightSpot == 4: gameGoing = False
                rightSpot = 0
                wrongSpot = 0
                userGuesses.insert(0, {"guesses": [], "rightEmojis": []})
            elif str(game.emoji) == "⬅️":
                if len(userGuesses) > 0: 
                    userGuesses[0]["guesses"].pop()
                    userGuesses[0]["guesses"] = userGuesses[0]["guesses"]
            else:
                if not len(userGuesses) > 0 or (len(userGuesses) > 0 and len(userGuesses[0]["guesses"]) > 4): userGuesses.insert(0, {"guesses": [], "rightEmojis": []})
                if not str(game.emoji) in userGuesses[0]["guesses"] or not len(userGuesses[0]["guesses"]) == 4: userGuesses[0]["guesses"].append(str(game.emoji))
                formattedGuesses = '\n'.join(f"{''.join(x['guesses'])} {''.join(filter(lambda y: y, x['rightEmojis']))}" for x in userGuesses[1:])
            await gameMessage.edit(f"Lives: {lives}\nYour guess:{''.join(userGuesses[0]['guesses'])}\n\n{formattedGuesses if len(userGuesses) >= 1 else ''}")
def setup(client):
    client.add_cog(MasterMind(client))