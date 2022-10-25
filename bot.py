# インストールした discord.py を読み込む
import asyncio
import os
import subprocess
import re

import discord
from discord.ext import commands

from voice_generator import creat_sound
#import command_list

# 自分のBotのアクセストークン
TOKEN = os.environ['TOKEN']

# 接続に必要なオブジェクトを生成
#intents = discord.Intents.all()
#intents.message_content = True

#client = discord.Client(intents=intents)

client = commands.Bot(command_prefix='>')
#client.remove_command("help")

#command_list(client)

# 作業ディレクトリをbot.pyが置いてあるディレクトリに変更
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ユーザ辞書
user_dic = []

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    activity = discord.Activity(name='>help', type=discord.ActivityType.playing)
    await client.change_presence(activity=activity)

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    # >始まりはコマンドとして処理。
    if message.content.startswith('>'):
        await client.process_commands(message)

    else:
        if message.guild.voice_client:
            inputText = ''

            #ユーザー名
            user = client.get_user(message.author.id).display_name + ' '
            inputText = user
            inputText = inputText + message.clean_content

            #メンション
            pattern = "<@/!.*>"
            inputText = re.sub(pattern,'',inputText)
            pattern = "@.* "
            inputText = re.sub(pattern,'',inputText)

            #print(inputText)
            creat_sound(inputText)
            source = discord.FFmpegPCMAudio("output.mp3",options="-af atempo=1.5")
            message.guild.voice_client.play(source)
        else:
            #ボイチャにこのbotが参加してなければ処理を飛ばす。
            pass

# >join
@client.command()
async def join(message):
    vc = message.author.voice.channel
    await vc.connect()
    await message.channel.send('にゃーん！(接続しました)')

# >bye
@client.command()
async def bye(message):
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

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)