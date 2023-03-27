# インストールした discord.py を読み込む
import os
from logging import getLogger

import discord
from discord.ext import commands

from voice_generator import creat_sound

logger = getLogger()

# 自分のBotのアクセストークン
TOKEN = os.environ['TOKEN']

# 接続に必要なオブジェクトを生成
intents = discord.Intents.all()

client = commands.Bot(command_prefix='$',intents=intents)
client.remove_command("help")

# 作業ディレクトリをbot.pyが置いてあるディレクトリに変更
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

    activity = discord.Activity(name='$help', type=discord.ActivityType.playing)
    await client.change_presence(activity=activity)

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    # >始まりはコマンドとして処理。
    if message.content.startswith('$'):
        await client.process_commands(message)

    else:
        if message.guild.voice_client:
            inputText = ''

            #ユーザー名
            user = client.get_user(message.author.id).display_name + ' '
            inputText = user

            inputText = inputText + message.clean_content

            creat_sound(inputText)
            source = discord.FFmpegPCMAudio("output.mp3",options="-af atempo=1.5")
            message.guild.voice_client.play(source)

        else:
            #ボイチャにこのbotが参加してなければ処理を飛ばす。
            pass

# voice状況が更新されたら入る
@client.event
async def on_voice_state_update(member, before, after):
    if member.guild.voice_client != None:
        if not member.bot and before.channel == None and after.channel != None :
            text = member.display_name+'が'+after.channel.name+'に接続しました。'
            creat_sound(text)
            source = discord.FFmpegPCMAudio("output.mp3",options="-af atempo=1.5")
            member.guild.voice_client.play(source)
            print(text)

# join
@client.command()
async def join(message):
    if message.author.voice is None:
        await message.channel.send("にゃーん！(あなたはボイスチャンネルに接続していません。)")
        return

    if message.guild.voice_client is not None:
        await message.channel.send("にゃーん！(既に接続しています。)")
        return

    await message.author.voice.channel.connect()
    await message.channel.send('にゃーん！(接続しました)')

# bye
@client.command()
async def bye(message):
    if message.guild.voice_client is None:
        await message.channel.send("にゃーん？(接続していません。)")
        return

    await message.voice_client.disconnect()
    await message.channel.send('にゃーん...(切断しました)')

# help
@client.command()
async def help(message):
    helpFile = open('./conf/help.txt', 'r', encoding='UTF-8')
    helpText = helpFile.read()
    await message.channel.send(helpText)
    helpFile.close()

@client.command()
async def stat(message):
    await message.channel.send('statコマンド実行者:'+client.get_user(message.author.id).display_name)

    vc_con_flg = True if message.guild.voice_client is not None else False
    await message.channel.send('ボイチャ接続:'+str(vc_con_flg))


# neko
@client.command()
async def neko(message):
    await message.channel.send('にゃーん')

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)