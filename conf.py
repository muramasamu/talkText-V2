"""
Voice Generator
~~~~~~~~~~~~~~~~~~~

文字列から音声を生成します。

"""
##import subprocess
import re
import io

from gtts import gTTS
import sql

def read_conf():
    """
    server設定を読み込み。
    """
    sqlstr = "select * from railway.conf"
    return sql.selectOne(sqlstr)

def update_conf(sqlstr):
    """
    server設定を更新。
    """
    sql.update(sqlstr)
