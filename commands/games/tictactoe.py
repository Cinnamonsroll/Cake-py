from discord.ext import commands
import discord
from discord_components import Button, ButtonStyle
class TicTacToe(commands.Cog):
    def __init__(self, client,):
        self.client = client
    @commands.command(name="tictactoe", aliases=["ttt"], description="Play tictactoe against another user", category="games",)
    async def ttt(self, ctx, member: discord.Member):
        if member == None or member.bot or member == ctx.message.author: return await ctx.send("Please include a valid user")
        board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        validating = True
        players = [
            {"member": ctx.message.author, "id": ctx.message.author.id, "symbol": "❌", "colour": "green"}
        ]
        validationMessage = await ctx.send(f"{ctx.message.author} would like to play a game of tictactoe aginst you, do you accept?", components=[
            [
                 Button(style=ButtonStyle.green, custom_id="Accept", label="Accept"),
                 Button(style=ButtonStyle.red, custom_id="Decline", label="Decline"),
            ]
        ])
        def flatten(t):
            return [item for sublist in t for item in sublist]
        def fullBoard():
            return len([x for x in flatten(board) if x in ["❌", "⭕"]]) == 9
        def checkWin():
          allPossibleWins = [[1, 2, 3],[4, 5, 6],[7, 8, 9],[1, 4, 7],[2, 5, 8],[3, 6, 9],[1, 5, 9],[3, 5, 7]]
          win = None
          flattenedBoard = flatten(board)
          for k in ["❌", "⭕"]:
              for w in allPossibleWins:
                  if len(list(filter(lambda x: x == k, [flattenedBoard[index - 1] for index in w]))) == 3: win = True
          return win
        async def startGame():
            game = True
            player = 0
            buttons = []
            for x in range(3):
                row = []
                for y in range(3):
                    row.append(Button(style=ButtonStyle.grey, custom_id=f"{x}:{y + 1}", label="\u200b"))
                buttons.append(row)
            gameMessage = await ctx.send(f"It is {players[player]['member']}\'s turn", components = buttons)
            while game:
                interactionGame = await self.client.wait_for("button_click", check = lambda x: x.user.id == players[player]["id"])
                xCord, yCord = interactionGame.custom_id.split(":")
                board[int(xCord)][int(yCord) - 1] = players[player]["symbol"]
                customButtons = []
                for x in range(3):
                    row = []
                    for y in range(3):
                        position = board[x][y]
                        row.append(Button(style=ButtonStyle.grey, emoji=position if not str(position).isnumeric() else self.client.get_emoji("862588317525606430"), disabled=True if not str(position).isnumeric() else False, custom_id=f"{x}:{y if not str(position).isnumeric() else (y + 1)}", label="\u200b"))
                    customButtons.append(row)
                if checkWin():
                    game = False
                    await interactionGame.respond(type=7, content=f"{players[player]['member']} won!",  components=customButtons)
                elif fullBoard():
                    game = False
                    await interactionGame.respond(type=7, content=f"It was a tie",  components=customButtons)
                else:
                    player = (player + 1) % len(players)
                    await interactionGame.respond(type=7, content=f"It is {players[player]['member']}\'s turn",  components=customButtons)
        while validating:
            interaction = await self.client.wait_for("button_click", check = lambda x: x.user.id == member.id)
            if interaction.custom_id == "Decline": 
                validating = False
                await interaction.respond("User has declined the game of tictactoe")
                await validationMessage.delete()
            elif interaction.custom_id == "Accept":
                await validationMessage.delete()
                validating = False
                players.append({"member": member, "id": member.id, "symbol": "⭕", "colour": "red"})
                await startGame()
def setup(client):
    client.add_cog(TicTacToe(client))