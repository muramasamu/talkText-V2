# インストールした discord.py を読み込む
import os
import re
from logging import getLogger

import discord
from discord.ext import commands

from voice_generator import creat_sound
import conf

logger = getLogger()

# 自分のBotのアクセストークン
TOKEN = os.environ['TOKEN']
print(TOKEN)

# 接続に必要なオブジェクトを生成
intents = discord.Intents.all()
#intents.message_content = True
#intents.menbers = True

#client = discord.Client(intents=intents)

client = commands.Bot(command_prefix='$',intents=intents)
client.remove_command("help")

#command_list(client)

# 作業ディレクトリをbot.pyが置いてあるディレクトリに変更
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ユーザ辞書
user_dic = []

# サーバごとの設定
server_conf_dict = {}

# 起動時に動作する処理
@client.event
async def on_ready():
    # サーバ設定読み込み
    global server_conf_dict
    server_conf_dict = conf.read_conf()

    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

    activity = discord.Activity(name='$help', type=discord.ActivityType.playing)
    await client.change_presence(activity=activity)

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    #print('message.author:'+message.author)
    #print('message.author.id:%s',message.author.id)
    #print('user name:%s',client.get_user(message.author.id))
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    # >始まりはコマンドとして処理。
    if message.content.startswith('$'):
        await client.process_commands(message)

    else:
        if message.guild.voice_client:
            inputText = ''

            #設定確認
            global server_conf_dict
            print("readnameFlg:"+str(server_conf_dict['readnameFlg']))
            print("readmentionFlg:"+str(server_conf_dict['readmentionFlg']))
            if 1 == server_conf_dict['readnameFlg']:
                print("ユーザー名を読み上げます")
                #ユーザー名
                user = client.get_user(message.author.id).display_name + ' '
                inputText = user

            print(message.clean_content)
            print(message.content)

            inputText = inputText + message.clean_content
            if 0 == server_conf_dict['readmentionFlg']:
                print("メンションを消します。")
                #メンション
                pattern = "<@/!.*>"
                inputText = re.sub(pattern,'',inputText)
                pattern = "@.* "
                inputText = re.sub(pattern,'',inputText)



            #print(inputText)
            # voice = creat_sound(inputText)
            # voice.seek(0)
            # source = discord.FFmpegPCMAudio(voice, pipe=True, options="-af atempo=1.5")
            # message.guild.voice_client.play(source)
            # voice.close()

            creat_sound(inputText)
            source = discord.FFmpegPCMAudio("output.mp3",options="-af atempo=1.5")
            message.guild.voice_client.play(source)

        else:
            #ボイチャにこのbotが参加してなければ処理を飛ばす。
            pass

# メッセージ受信時に動作する処理
@client.event
async def on_voice_state_update(member, before, after):
    if not member.bot and before.channel == None and after.channel != None : #and member.guild.voice_client
        text = member.display_name+'が'+after.channel.name+'に接続しました。'
        creat_sound(text)
        source = discord.FFmpegPCMAudio("output.mp3",options="-af atempo=1.5")
        member.guild.voice_client.play(source)
        print(text)

# join
@client.command()
async def join(message):
    vc = message.author.voice.channel
    await vc.connect()
    await message.channel.send('にゃーん！(接続しました)')

# bye
@client.command()
async def bye(message):
    await message.voice_client.disconnect()
    await message.channel.send('にゃーん...(切断しました)')

# help
@client.command()
async def help(message):
    helpFile = open('./conf/help.txt', 'r', encoding='UTF-8')
    helpText = helpFile.read()
    await message.channel.send(helpText)
    helpFile.close()

# neko
@client.command()
async def neko(message):
    await message.channel.send('にゃーん')

# readname
@client.command()
async def readname(message, arg):
    if arg == 'on':
        sql = "UPDATE railway.conf SET readnameFlg = 1"
        conf.update_conf(sql)
        server_conf_dict['readnameFlg']=1
        await message.channel.send('readnameをONにしました')
    elif arg == 'off':
        sql = "UPDATE railway.conf SET readnameFlg = 0"
        conf.update_conf(sql)
        server_conf_dict['readnameFlg']=0
        await message.channel.send('readnameをOFFにしました')
    else:
        await message.channel.send('"on"か"off"しか受け付けません')

# readmention
@client.command()
async def readmention(message, arg):
    if arg == 'on':
        sql = "UPDATE railway.conf SET readmentionFlg = 1"
        conf.update_conf(sql)
        server_conf_dict['readmentionFlg']=1
        await message.channel.send('readmentionをONにしました')
    elif arg == 'off':
        sql = "UPDATE railway.conf SET readmentionFlg = 0"
        conf.update_conf(sql)
        server_conf_dict['readmentionFlg']=0
        await message.channel.send('readmentionをOFFにしました')
    else:
        await message.channel.send('"on"か"off"しか受け付けません')

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)