import discord
from discord.ext import commands
import traceback
import json
import aiobungie
import auth
import os
import asyncio

# OAuth Information

# Discord Bot Client
client = commands.Bot(command_prefix=">", case_insensitive=True)


@client.event
async def on_ready():
    print("Lil Light in da house")
    test_channel = client.get_channel(795189216304037889)
    await test_channel.send("Lil Light in da house")


@client.event
async def on_disconnect():
    print("Little Light is off")
    test_channel = client.get_channel(795189216304037889)
    await test_channel.send("Little Light disconnected")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    elif "raid" in message.content.lower():
        response = "RAID"
        await message.channel.send(response)

    await client.process_commands(message)


# commands
@client.command()
async def pog(ctx):  # function name is the command to respond to
    # This is the bot's response
    try:
        await ctx.send("pog indeed", file=discord.File('images/flop.jpg'))

    except Exception as e:
        print(e)
        await ctx.send("something went wrong I might not have upload file permissions")


@client.command()
async def join(ctx):
    try:
        async with auth.client.acquire() as rest:
            text_file = open("placeholder.txt", "r")
            token = text_file.read()
            print(token)
            text_file.close()
            my_user = await rest.fetch_current_user_memberships(token)
            await ctx.send(my_user.get("bungieNetUser").get("uniqueName"))

    except Exception as e:
        print(e)
        pass


@client.command()
async def generate_oauth_url(ctx):
    try:
        url = auth.combinational_logic_get_oauth2_url(ctx.author.name)
        await ctx.author.send(url)

    except Exception as e:
        print(e)
        await ctx.send("Error check logs")


@client.command()
async def indeed(ctx):  # function name is the command to respond to
    # This is the bot's response
    try:
        await ctx.send("indeed",
                       file=discord.File('images/Indeed.gif'))  # *""* for italics \* escape slash to just use the icon

    except:
        await ctx.send("something went wrong I might not have upload file permissions")


@client.command()
async def version(ctx):
    try:
        myEmbed = discord.Embed(title="Current Version", description="Version is 1.0",
                                color=0x00ff00)  # color is hex for RGB RRGGBB so completely green == 00ff00
        myEmbed.add_field(name="Version Code:", value="v1.0.0", inline=False)
        myEmbed.add_field(name="Date Released:", value="11/26/2020", inline=False)
        myEmbed.set_footer(text="Sample Footer")
        myEmbed.set_author(name="Jonesdebu", url="https://github.com/jonesdebu?tab=repositories",
                           icon_url="https://github.githubassets.com/images/modules/open_graph/github-mark.png ")
        await ctx.send(embed=myEmbed)

    except:
        await ctx.send("Something went wrong I might not have embed permissions")


@client.command()
async def info(ctx):
    try:
        myEmbed = discord.Embed(title="Help", description="Commands",
                                color=0x000055)  # color is hex for RGB RRGGBB so completely green == 00ff00
        myEmbed.add_field(name="Get Bot Version:", value=">Version", inline=False)
        myEmbed.add_field(name="Pog On Demand:", value=">Pog", inline=False)
        myEmbed.add_field(name="Indeed On Demand:", value=">Indeed", inline=False)
        myEmbed.set_footer(text="Little Light")
        file = discord.File("images/D2Icon.png")
        myEmbed.set_image(url="attachment://D2Icon.png")
        myEmbed.set_author(name="Jonesdebu", url="https://github.com/jonesdebu?tab=repositories",
                           icon_url="https://github.githubassets.com/images/modules/open_graph/github-mark.png ")
        await ctx.send(file=file, embed=myEmbed)

    except Exception:
        traceback.print_exc()
        await ctx.send("Something went wrong I might not have embed permissions")


client.run(os.environ.get("Discord_Bot_Token"))
