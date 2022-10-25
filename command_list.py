"""
Command List
~~~~~~~~~~~~~~~~~~~

投げられるコマンドをまとめます。

"""
# インストールした discord.py を読み込む
import asyncio
import os
import subprocess
import re

from threading import Thread

import discord
from discord.ext import commands

client = None

def setInfo(clientObj):
    global client
    client = clientObj

# >join
@client.command()
async def join(message):
    print('#voicechannelを取得')
    vc = message.author.voice.channel
    print('#voicechannelに接続')
    await vc.connect()
    await message.channel.send('にゃーん！(接続しました)')

# >bye
@client.command()
async def bye(message):
    print('#切断')
    await message.voice_client.disconnect()
    await message.channel.send('にゃーん...(切断しました)')

# >help
@client.command()
async def help(message):
    helpFile = open('./text/help.txt', 'r', encoding='UTF-8')
    helpText = helpFile.read()
    await message.channel.send(helpText)
    helpFile.close()

# >neko
@client.command()
async def neko(message):
    await message.channel.send('にゃーん')