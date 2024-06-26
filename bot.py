import discord
from discord.ext import commands
import traceback
import json
import aiobungie
from aiobungie.internal import enums
import auth
import os
import asyncio
from db import db_get_auth  # Need to implement auth check for bot commands that require oauth2
from test import get_characters, get_characters_stats
from pymongo import MongoClient

# OAuth Information

# Discord Bot Client
intents = discord.Intents.all()
intents.messages = True
intents.dm_messages = True


client = commands.Bot(command_prefix=">", case_insensitive=True, intents=intents)

aiobungie_client = aiobungie.Client(os.environ.get("api_key"))


@client.event
async def on_ready():
    print("Lil Light")
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
async def test(ctx):  # function name is the command to respond to
    # This is the bot's response
    try:
        await ctx.send("test")

    except Exception as e:
        print(e)
        await ctx.send("something went wrong I might not have permissions")


@client.command()
async def join(ctx):
    try:
        user = db_get_auth(ctx.author.name)
        if user:
            await ctx.send(user)
        else:
            await ctx.send("You must sign up first")

    except Exception as e:
        print(e)
        pass


@client.command()
async def register(ctx):
    try:
        if db_get_auth(ctx.author.name):
            await ctx.send("You are already a user")
        else:
            url = auth.combinational_logic_get_oauth2_url(ctx.author.name)
            await ctx.send("Check your messages for the registration link")
            await ctx.author.send(f"Follow this link and sign in to register: {url}")

    except Exception as e:
        print(e)
        await ctx.send("Error check logs")


async def build_character_embed(class_type, character):
    char_embed = discord.Embed(title=class_type)
    char_embed.set_image(url=character['emblem'])
    char_embed.add_field(name='Light', value=character['light'], inline=False)
    char_embed.add_field(name='Level', value=character['level'], inline=False)
    char_embed.add_field(name='Gender', value=character['gender'], inline=False)
    char_embed.add_field(name='Race', value=character['race'], inline=False)
    char_embed.add_field(name='Total Time Played', value=character['total_played_time'], inline=False)
    char_embed.set_thumbnail(url=character['emblem_icon'])
    return char_embed


async def build_character_stats_embed(class_type, content):
    print(content)
    stat_embed = discord.Embed(title=class_type)
    stat_embed.add_field(name='Mobility', value=content['MOBILITY'], inline=False)
    stat_embed.add_field(name='Recovery', value=content['RECOVERY'], inline=False)
    stat_embed.add_field(name='Resilience', value=content['RESILIENCE'], inline=False)
    stat_embed.add_field(name='Intellect', value=content['INTELLECT'], inline=False)
    stat_embed.add_field(name='Strength', value=content['STRENGTH'], inline=False)
    stat_embed.add_field(name='Discipline', value=content['DISCIPLINE'], inline=False)
    return stat_embed


@client.command()
async def eyesupguardian(ctx):
    try:
        if db_get_auth(ctx.author.name):
            mongo_client = MongoClient(os.environ.get("MONGO_CONNECTION_URL"))
            user = mongo_client['Little-Light']['Users'].find_one({"discordName": ctx.author.name})
            mongo_client.close()
            mem_id = user.get("membershipId")
            chars = await get_characters(user.get("membershipId"), user.get("membershipType"),
                                         [aiobungie.ComponentType.CHARACTERS])
            for class_type, content in chars.items():
                my_embed = await build_character_embed(class_type, content)
                await ctx.send(embed=my_embed)

        else:
            await ctx.send("You must sign up first")

    except Exception as e:
        print(e)


@client.command()
async def buildstats(ctx):
    try:
        if db_get_auth(ctx.author.name):
            mongo_client = MongoClient(os.environ.get("MONGO_CONNECTION_URL"))
            user = mongo_client['Little-Light']['Users'].find_one({"discordName": ctx.author.name})
            mongo_client.close()
            mem_id = user.get("membershipId")
            chars = await get_characters_stats(user.get("membershipId"), user.get("membershipType"),
                                               [aiobungie.ComponentType.CHARACTERS])
            for class_type, content in chars.items():
                my_embed = await build_character_stats_embed(class_type, content)
                await ctx.send(embed=my_embed)

        else:
            await ctx.send("You must sign up first")
    except Exception as e:
        print(e)


@client.command()
async def indeed(ctx):  # function name is the command to respond to
    # This is the bot's response
    try:
        await ctx.send("indeed",
                       file=discord.File('images/Indeed.gif'))  # *""* for italics \* escape slash to just use the icon

    except Exception as e:
        print(e)
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

    except Exception as e:
        print(e)
        await ctx.send("Something went wrong I might not have embed permissions")


@client.command()
async def info(ctx):
    try:
        myEmbed = discord.Embed(title="Help", description="Commands",
                                color=0x000055)  # color is hex for RGB RRGGBB so completely green == 00ff00
        myEmbed.add_field(name="Get Join Code:", value=">join", inline=False)
        myEmbed.add_field(name="Get Bot Version:", value=">Version", inline=False)
        myEmbed.add_field(name="Pog On Demand:", value=">Pog", inline=False)
        myEmbed.add_field(name="Indeed On Demand:", value=">Indeed", inline=False)
        myEmbed.set_footer(text="Little Light")
        file = discord.File("images/D2Icon.png")
        myEmbed.set_image(url="attachment://D2Icon.png")
        myEmbed.set_author(name="Jonesdebu", url="https://github.com/jonesdebu?tab=repositories",
                           icon_url="https://github.githubassets.com/images/modules/open_graph/github-mark.png ")
        await ctx.send(file=file, embed=myEmbed)

    except Exception as e:
        print(e)
        traceback.print_exc()
        await ctx.send("Something went wrong I might not have embed permissions")


client.run(os.environ.get("Discord_Bot_Token"))
