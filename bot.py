import discord
from discord.ext import commands
import requests
import pydest
import os
from dotenv import load_dotenv
import traceback
#import json


#OAuth Information
load_dotenv()

apikey = os.getenv("apikey")
OAuth_client_id = os.getenv("Oauth_Client_Id")
bungoAuthURI = "https://www.bungie.net/en/OAuth/Authorize?client_id=" + OAuth_client_id + "&response_type=code"
apiheaders = {'X-API-Key': apikey}
destiny = pydest.Pydest(apikey)


#Discord Bot Client
client = commands.Bot(command_prefix=">", case_insensitive=True)

@client.event
async def on_ready():
    print("Pog Bot is ready")
    print(bungoAuthURI)
    test_channel = client.get_channel(781576402931417089)
    await test_channel.send("Little Light is here")

@client.event
async def on_disconnect():
    print("Bog Bot is off")
    await destiny.close()
    test_channel = client.get_channel(781576402931417089)
    await test_channel.send("Little Light disconnected")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if "atraks" in message.content.lower():
        response = "**BEEP BOOP* \* fuck atraks"
        await message.channel.send(response, file = discord.File('images/Atraks.jpg'))

    elif "raid" in message.content.lower():
        response = "RAID"
        await message.channel.send(response)

    await client.process_commands(message)

#commands
@client.command()
async def pog(ctx): #function name is the command to respond to
    # This is the bot's response
    try:
        await ctx.send("\**BEEP BOOP* \* pog indeed", file=discord.File('images/flop.jpg'))

    except:
        await ctx.send("something went wrong I might not have upload file permissions")



@client.command()
async def indeed(ctx): #function name is the command to respond to
    # This is the bot's response
    try:
        await ctx.send("\**BEEP BOOP* \* indeed", file=discord.File('images/Indeed.gif')) # *""* for italics \* escape slash to just use the icon

    except:
        await ctx.send("something went wrong I might not have upload file permissions")

@client.command()
async def get(ctx, username=None):
    if not username:
        await ctx.send('\**BEEP BOOP* \* Please enter a valid username after the command')
        return
    try:
        id_json = await destiny.api.search_destiny_player(3, username)
        membership_id = id_json['Response'][0]['membershipId']
        print(membership_id)
        myComponents = [200]
        profile_json = await destiny.api.get_profile(3, membership_id, myComponents) #platform replaced by a variable
        print(profile_json)
        charData = profile_json['Response']['characters']['data']
        playerChars = list(charData.keys())
        testFirstCharLight = charData[playerChars[0]]['light']
        #print(testFirstCharLight)
        await ctx.send('\**BEEP BOOP* \* Your first character\'s light level is: ' + str(testFirstCharLight)) # return the first character's light level


    except (IndexError, KeyError) as e:
        print(e)
        await ctx.send('\**BEEP BOOP* \* User not found.')
        raise


@client.command()
async def version(ctx):
    try:
        myEmbed = discord.Embed(title="Current Version", description="Version is 1.0", color=0x00ff00) #color is hex for RGB RRGGBB so completely green == 00ff00
        myEmbed.add_field(name="Version Code:", value="v1.0.0", inline=False)
        myEmbed.add_field(name="Date Released:", value="11/26/2020", inline=False)
        myEmbed.set_footer(text="Sample Footer")
        myEmbed.set_author(name="Neo", url="https://github.com/jonesdebu?tab=repositories", icon_url="https://github.githubassets.com/images/modules/open_graph/github-mark.png ")
        await ctx.send(embed=myEmbed)

    except:
        await ctx.send("Something went wrong I might not have embed permissions")

@client.command()
async def info(ctx):
    try:
        myEmbed = discord.Embed(title="Help", description="Commands", color=0x000055) #color is hex for RGB RRGGBB so completely green == 00ff00
        myEmbed.add_field(name="Get Bot Version:", value=">Version", inline=False)
        myEmbed.add_field(name="Pog On Demand:", value=">Pog", inline=False)
        myEmbed.add_field(name="Indeed On Demand:", value=">Indeed", inline=False)
        myEmbed.set_footer(text="Little Light")
        file = discord.File("images/D2Icon.png")
        myEmbed.set_image(url="attachment://D2Icon.png")
        myEmbed.set_author(name="Neo", url="https://github.com/jonesdebu?tab=repositories", icon_url="https://github.githubassets.com/images/modules/open_graph/github-mark.png ")
        await ctx.send(file=file, embed=myEmbed)

    except Exception:
        traceback.print_exc()
        await ctx.send("Something went wrong I might not have embed permissions")






client.run(os.getenv("Discord-Bot-Token"))
