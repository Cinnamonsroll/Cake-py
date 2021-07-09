from discord_components import (
    DiscordComponents,
    Button,
    ButtonStyle,
    Select,
    SelectOption,
)
def createButtons(disabledComponents, client, embedsLen): 
    if embedsLen > 1:
        return  [
        [
            Button(style=ButtonStyle.red, disabled=disabledComponents, custom_id="Delete", label="\u200b", emoji=client.get_emoji(848216792845516861)),
            Button(style=ButtonStyle.blue, disabled=disabledComponents, custom_id="Backward", label="\u200b", emoji=client.get_emoji(848237448269135924)),
            Button(style=ButtonStyle.blue, disabled=disabledComponents, custom_id="Stop", label="\u200b", emoji=client.get_emoji(848633645123371038)),
            Button(style=ButtonStyle.blue, disabled=disabledComponents, custom_id="Forward", label="\u200b", emoji=client.get_emoji(848237230363246612)),
        ]
    ]
    else: return  [
        [
            Button(style=ButtonStyle.red, disabled=disabledComponents, custom_id="Delete", label="\u200b", emoji=client.get_emoji(848216792845516861)),
        ]
    ]
async def pagination(client, ctx, message, embeds):
    page = 0
    going = True
    disabledComponents = False
    mainMessage = await ctx.send(embed=embeds[page], components=createButtons(False, client, len(embeds)))
    while going:
        interaction = await client.wait_for("button_click", check = lambda x: x.user.id == message.author.id)
        if interaction.custom_id == "Delete":
            going = False
            return await mainMessage.delete()
        elif interaction.custom_id == "Backward":
            if page == 0: page = len(embeds) - 1
            else: page -= 1
        elif interaction.custom_id == "Stop":
            going = False
            disabledComponents = True
        elif interaction.custom_id == "Forward":
            if page == len(embeds) - 1: page = 0
            else: page += 1
        await interaction.respond(type=7, embed=embeds[page], components=createButtons(disabledComponents, client, len(embeds)))