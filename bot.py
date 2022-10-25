# インストールした discord.py を読み込む
import asyncio
import os
import subprocess
import re

from threading import Thread

import discord
from discord.ext import commands

from voice_generator import creat_sound
from command import set

# 自分のBotのアクセストークン
TOKEN = os.environ['TOKEN']

# 接続に必要なオブジェクトを生成
client = commands.Bot(command_prefix='>')
client.remove_command("help")

# 作業ディレクトリをbot.pyが置いてあるディレクトリに変更
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ユーザ辞書
user_dic = []

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    set(client)
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
            if flg.readname_flg :
                user = client.get_user(message.author.id).display_name + ' '
                inputText = user
            inputText = inputText + message.clean_content
            if not flg.readmention_flg :
                pattern = "<@/!.*>"
                inputText = re.sub(pattern,'',inputText)
                pattern = "@.* "
                inputText = re.sub(pattern,'',inputText)
            #print(inputText)
            creat_sound(inputText)
            source = discord.FFmpegPCMAudio("output.mp3",options="-af atempo=1.5")
            message.guild.voice_client.play(source)
        else:
            pass


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)