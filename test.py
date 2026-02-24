import os
from dotenv import load_dotenv

load_dotenv()




import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# ===== Google Sheets 認証 =====
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

import os
import base64
import json

encoded = os.environ["GOOGLE_CREDENTIALS_BASE64"]

decoded_bytes = base64.b64decode(encoded)
decoded_str = decoded_bytes.decode("utf-8")

creds_dict = json.loads(decoded_str)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

client = gspread.authorize(creds)
sheet = client.open("勤怠管理").sheet1

# ===== Discord Bot 設定 =====
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"ログイン成功: {bot.user}")

TARGET_CHANNEL_ID = 1473898209381191858

@bot.event
async def on_message(message):

    if message.author.bot:
        return

    if message.channel.id != TARGET_CHANNEL_ID:
        return

from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+

now_jst = datetime.now(ZoneInfo("Asia/Tokyo"))
date_str = now_jst.strftime("%Y-%m-%d")
time_str = now_jst.strftime("%H:%M:%S")






    if "おはよう" in message.content:
        sheet.append_row([
            message.author.display_name,
            date,
            time,
            "出勤"
        ])
        await message.channel.send("出勤を記録しました！")

    elif "お疲れ" in message.content:
        sheet.append_row([
            message.author.display_name,
            date,
            time,
            "退勤"
        ])
        await message.channel.send("退勤を記録しました！")

    await bot.process_commands(message)

bot.run(os.environ["DISCORD_TOKEN"])
