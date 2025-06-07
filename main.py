from unittest.mock import patch
import telebot
from telebot import types
import signal
import os
import gc
import psutil
import subprocess
import threading
import datetime
import time
import json
import ast
import sys
import shutil
import re
import datetime
import time
import argparse
import html
import getpass  # 🔐 Secure password input (invisible

# Accept bot token from command-line
parser = argparse.ArgumentParser()
parser.add_argument('--token', help='Custom bot token')
parser.add_argument('--owner', type=int, help='Owner Telegram ID')
parser.add_argument('--admins', help='Comma-separated Admin IDs')
args = parser.parse_args()

# 📅 Set your desired expiry date here
#expiry_date = datetime.date(2025, 6, 14)
#if datetime.date.today() > expiry_date:
  #  print("⛔ 𝚃𝙷𝙴 𝚂𝙲𝚁𝙸𝙿𝚃 𝙷𝙰𝚂 𝙱𝙴𝙴𝙽 𝙴𝚇𝙿𝙸𝚁𝙴𝙳 𝙿𝙻𝙴𝙰𝚂𝙴 𝙲𝙾𝙽𝚃𝙰𝙲𝚃 𝚃𝙾 𝙳𝙴𝚅𝙴𝙻𝙾𝙿𝙴𝚁 @SP1DEYYXPR1ME.")
    #sys.exit()

# 🔐 Stylish Startup Password
#𝙎𝙀𝘾𝙍𝙀𝙏_𝙋𝘼𝙎𝙎𝙒𝙊𝙍𝘿 = "SP1DEYYXPR1ME"  # ← Apna stylish password yahaan likho

# 🛡️ Invisible password input
#𝙞𝙣𝙥𝙪𝙩_𝙥𝙖𝙨𝙨 = getpass.getpass("🔐 𝙀𝙉𝙏𝙀𝙍 𝘽𝙊𝙏 𝘼𝘾𝘾𝙀𝙎𝙎 𝙋𝘼𝙎𝙎𝙒𝙊𝙍𝘿 🗝️: ").strip()

#if 𝙞𝙣𝙥𝙪𝙩_𝙥𝙖𝙨𝙨 != 𝙎𝙀𝘾𝙍𝙀𝙏_𝙋𝘼𝙎𝙎𝙒𝙊𝙍𝘿:
#    print("❌ 𝙒𝙍𝙊𝙉𝙂 𝙋𝘼𝙎𝙎𝙒𝙊𝙍𝘿! 𝙔𝙊𝙐 𝘼𝙍𝙀 𝙉𝙊𝙏 𝘼𝙐𝙏𝙃𝙊𝙍𝙄𝙕𝙀𝘿 ❌")
  #  sys.exit(1)

 #✅ Runtime BOT Setup
TOKEN = args.token if args.token else input("🤖 𝙀𝙉𝙏𝙀𝙍 𝙔𝙊𝙐𝙍 𝘽𝙊𝙏 𝙏𝙊𝙆𝙀𝙉: ").strip()
if not TOKEN or " " in TOKEN or ":" not in TOKEN:
    print("❌ 𝙄𝙉𝙑𝘼𝙇𝙄𝘿 𝘽𝙊𝙏 𝙏𝙊𝙆𝙀𝙉! Example: 123456:ABCDEF...")
    sys.exit(1)

if args.owner:
    OWNER_ID = args.owner
else:
    try:
        OWNER_ID = int(input("👤 𝙀𝙉𝙏𝙀𝙍 𝙊𝙒𝙉𝙀𝙍 𝙄𝘿: ").strip())
    except ValueError:
        print("❌ 𝙄𝙉𝙑𝘼𝙇𝙄𝘿 𝙊𝙒𝙉𝙀𝙍 𝙄𝘿! It must be a number.")
        #sys.exit(1)

if args.admins:
    admin_parts = [x.strip() for x in args.admins.split(",")]
else:
    admin_input = input("👑 𝙀𝙉𝙏𝙀𝙍 𝘼𝘿𝙈𝙄𝙉 𝙄𝘿𝙨 (comma-separated): ").strip()
    admin_parts = [x.strip() for x in admin_input.split(",")]

ADMINS = []
for x in admin_parts:
    if not x.isdigit():
        print(f"❌ 𝙄𝙉𝙑𝘼𝙇𝙄𝘿 𝘼𝘿𝙈𝙄𝙉 𝙄𝘿: {x} (must be numbers only)")
        sys.exit(1)
    ADMINS.append(int(x))

# ✅ Confirm collected input
print(f"✅ BOT TOKEN: {TOKEN[:6]}******")
print(f"✅ OWNER ID: {OWNER_ID}")
print(f"✅ ADMINS: {ADMINS}")

def escape_markdown(text):
    """
    Escapes only special characters required by MarkdownV2 format.
    Does not escape valid characters like dots or slashes in file names.
    """
    return re.sub(r'([_*[\]()~`>#+\-=|{}.!])', r'\\\1', text)

#OWNER_ID = 6675486524  # Apna Telegram ID yahan daalein

OWNER_ID = 6675486524  # Replace with your actual ID
ADMIN_ID = 6675486524

# ✅ Step 2: THEN this line should come
TOKEN = args.token if args.token else "7726101448:AAHrXN9dfkYUwVW7KwM1JXOuZnXdl_pNVV8"
bot = telebot.TeleBot(TOKEN)

def admin_only(func):
    def wrapper(message, *args, **kwargs):
        if message.from_user.id not in ADMINS and message.from_user.id != OWNER_ID:
            bot.reply_to(message, "❌ 𝙔𝙊𝙐 𝘼𝙍𝙀 𝙉𝙊𝙏 𝘼𝙐𝙏𝙃𝙊𝙍𝙄𝙕𝙀𝘿 𝙏𝙊 𝙐𝙎𝙀 𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿 ⚡.")
            return
        return func(message, *args, **kwargs)
    return wrapper

def owner_only(func):
    def wrapper(message, *args, **kwargs):
        if message.from_user.id != OWNER_ID:
            bot.reply_to(message, "❌ 𝙔𝙊𝙐 𝘼𝙍𝙀 𝙉𝙊𝙏 𝘼𝙐𝙏𝙃𝙊𝙍𝙄𝙕𝙀𝘿 𝙏𝙊 𝙐𝙎𝙀 𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿 ⚡.")
            return
        return func(message, *args, **kwargs)
    return wrapper

# Default or custom token
# ✅ Step 1: FIRST paste this block
CLONED_BOTS_FILE = "cloned_bots.json"

if os.path.exists(CLONED_BOTS_FILE):
    with open(CLONED_BOTS_FILE) as f:
        cloned_bots = json.load(f)
else:
    cloned_bots = []
   
ACCESS_PASSWORD = "SP1DEYYGOD"

APPROVED_USERS_FILE = "approved_users.json"
PREMIUM_USERS_FILE = "premium_users.json"
ADMINS_FILE = "admins.json"
CLONED_BOTS_FILE = "cloned_bots.json"

# Load users
if os.path.exists(PREMIUM_USERS_FILE):
    with open(PREMIUM_USERS_FILE) as f:
        premium_users = json.load(f)
else:
    premium_users = []

if os.path.exists(APPROVED_USERS_FILE):
    with open(APPROVED_USERS_FILE) as f:
        approved_users = json.load(f)
else:
    approved_users = []

if os.path.exists(ADMINS_FILE):
    with open(ADMINS_FILE) as f:
        ADMINS = json.load(f)
else:
    ADMINS = []

if os.path.exists(CLONED_BOTS_FILE):
    with open(CLONED_BOTS_FILE) as f:
        cloned_bots = json.load(f)
else:
    cloned_bots = []

# Save functions
def save_premium_users():
    with open(PREMIUM_USERS_FILE, "w") as f:
        json.dump(premium_users, f)

def save_approved_users():
    with open(APPROVED_USERS_FILE, "w") as f:
        json.dump(approved_users, f)

def save_admins():
    with open(ADMINS_FILE, "w") as f:
        json.dump(ADMINS, f)

def save_cloned_bots():
    with open(CLONED_BOTS_FILE, "w") as f:
        json.dump(cloned_bots, f)

# Check functions
def is_premium(user_id):
    return user_id in premium_users or user_id in ADMINS

def is_approved(user_id):
    return user_id in approved_users or user_id in ADMINS

# 🔄 Notify owner if this bot is a clone
if args.token:  # Means this is a cloned bot
# ✅ Cloned bot: override owner/admins
    if args.owner:
        OWNER_ID = args.owner

    if args.admins:
        ADMINS = [int(x.strip()) for x in args.admins.split(",") if x.strip().isdigit()]
       
    approved_users = []
    ADMINS = []       

    # ✅ Give cloned owner full access
    if OWNER_ID not in approved_users:
        approved_users.append(OWNER_ID)
        save_approved_users()

    if OWNER_ID not in ADMINS:
        ADMINS.append(OWNER_ID)
        save_admins()
    try:
        import html
        now = html.escape(datetime.datetime.now().strftime("%d %b, %Y — %I:%M %p"))

        bot.send_message(
            OWNER_ID,
            (
                "╔════════════════════════════╗\n"
                "𝙲𝙻𝙾𝙽𝙴𝙳 𝙱𝙾𝚃 𝚂𝚃𝙰𝚁𝚃𝙴𝙳 𝚂𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈 ✅\n"
                "╚════════════════════════════╝\n\n"
                "<b>🟢 𝚂𝚃𝙰𝚃𝚄𝚂:</b> <code>𝚁𝚄𝙽𝙽𝙸𝙽𝙶</code>\n"
                f"<b>📅 𝙳𝙰𝚃𝙴:</b> <code>{now}</code>\n\n"
                "<b>👤 𝙲𝙻𝙾𝙽𝙴𝙳 𝙱𝚈:</b> <a href='https://t.me/SP1DEYYXPR1ME'>@SP1DEYYXPR1ME</a>\n"
                "<b>🔗 𝙲𝙻𝙾𝙽𝙴 𝙾𝙵:</b> <a href='https://t.me/PythonFileHoster'>@PythonFileHoster</a>\n\n"
                "⚡ <i>𝚃𝙷𝙸𝚂 𝙸𝚂 𝙰 𝙱𝙾𝚃 𝙲𝙻𝙾𝙽𝙴𝙳 𝙱𝚈</i> <b>@SP1DEYYXPR1ME</b>"
            ),
            parse_mode='HTML'
        )

    except Exception as e:
        print(f"❌ Failed to send clone startup message: {e}")
       
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, f"uploads_{TOKEN[:10]}")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

processes = {}
cloned_bots = []
clone_processes = []  # To track cloned bot processes
MAX_FILE_SIZE = 5 * 1024 * 1024
EXECUTION_TIMEOUT = 300
START_TIME = time.time()
file_upload_count = 0

scheduled_jobs = {}  # job_id -> {'user_id', 'filename', 'run_time'}
ADMINS_FILE = "admins.json"
if os.path.exists(ADMINS_FILE):
    with open(ADMINS_FILE) as f:
        ADMINS = json.load(f)
else:
    ADMINS = [6675486524]  # List of admin user IDs
# ✅ Main bot: Hardcoded owner/admin (you)
OWNER_ID = 6675486524  # ← Replace with your actual Telegram ID
ADMINS = [6675486524]  # ← You are sole admin in main bot

# Define owner separately
OWNER_ID = 6675486524  # Apna Telegram ID yahan daalein
# 🔓 Automatically give owner full access
if OWNER_ID not in approved_users:
    approved_users.append(OWNER_ID)
    save_approved_users()

if OWNER_ID not in ADMINS:
    ADMINS.append(OWNER_ID)
    save_admins()

user_clone_context = {}

# ⚡ Auto-restart all previously cloned bots (only if this is the main bot)
if not args.token:  # Ensure this is the main (not a clone) bot
    for bot_info in cloned_bots:
        token = bot_info.get("token")
        if token:
            try:
                print(f"🚀 Restarting cloned bot: {token[:6]}******")
                log_path = os.path.join(LOGS_DIR, f"{token[:10]}_clone.log")
                with open(log_path, 'w') as log_file:
                    process = subprocess.Popen(
                        [sys.executable, __file__,
                         '--token', token,
                         '--owner', str(OWNER_ID),
                         '--admins', ','.join(map(str, ADMINS))],
                        stdout=log_file,
                        stderr=log_file
                    )
                    clone_processes.append(process)
            except Exception as e:
                print(f"❌ Failed to restart bot {token[:6]}... — {e}")

#def check_password(message):
    #if message.text == ACCESS_PASSWORD:
       # approved_users.append(message.from_user.id)
    #    save_approved_users()
       # bot.reply_to(message, "✅ 𝘼𝘾𝘾𝙀𝙎𝙎 𝙂𝙍𝘼𝙉𝙏𝙀𝘿 ⚡\n\n𝙒𝙀𝙇𝘾𝙊𝙈𝙀 𝙏𝙊 𝙏𝙃𝙀 𝘽𝙊𝙏!")
        # Optionally: Call /start again
        #start_command(message)
   # else:
        #bot.reply_to(message, "❌ 𝙄𝙉𝙑𝘼𝙇𝙄𝘿 𝙋𝘼𝙎𝙎𝙒𝙊𝙍𝘿 🔐\n\n𝙏𝙍𝙔 𝘼𝙂𝘼𝙄𝙉 𝘽𝙔 𝙎𝙀𝙉𝘿𝙄𝙉𝙂 /start")
  
# Block unapproved users from using any command
@bot.message_handler(func=lambda message: not is_approved(message.from_user.id))
def reject_unapproved_users(message):
    bot.reply_to(message, "❌ 𝙔𝙊𝙐 𝘼𝙍𝙀 𝙉𝙊𝙏 𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝘿 𝙏𝙊 𝙐𝙎𝙀 𝙏𝙃𝙄𝙎 𝘽𝙊𝙏⚡.")
    print(f"[BLOCKED] Unapproved message from: {message.from_user.id}")

# Block unapproved users from pressing any buttons
@bot.callback_query_handler(func=lambda call: not is_approved(call.from_user.id))
def reject_unapproved_callbacks(call):
    bot.answer_callback_query(call.id, "❌ 𝙔𝙊𝙐 𝘼𝙍𝙀 𝙉𝙊𝙏 𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝘿.")
    print(f"[BLOCKED] Callback attempt by: {call.from_user.id}")

@bot.message_handler(commands=['start'])
def start_command(message):   
    user_id = message.from_user.id

    if not is_approved(user_id):
        ask = bot.send_message(
            message.chat.id,
            "🔐 𝙀𝙉𝙏𝙀𝙍 𝙏𝙃𝙀 𝘼𝘾𝘾𝙀𝙎𝙎 𝙋𝘼𝙎𝙎𝙒𝙊𝙍𝘿 🗝️\n\n𝙏𝙊 𝙐𝙉𝙇𝙊𝘾𝙆 𝙏𝙃𝙄𝙎 𝘽𝙊𝙏 ⚡\n@SP1DEYYXPR1ME"
        )
        bot.register_next_step_handler(ask, check_password)
        return

    loading_msg = bot.send_message(message.chat.id, "𝙇𝙊𝘼𝘿𝙄𝙉𝙂 ⚡...")
    
    welcome_stages = [
        "𝙇𝙊𝘼𝘿𝙄𝙉𝙂 ⚡ ▒▒▒▒▒▒▒▒▒▒ 0%",
        "𝙇𝙊𝘼𝘿𝙄𝙉𝙂 ⚡ █▒▒▒▒▒▒▒▒▒ 10%",
        "𝙇𝙊𝘼𝘿𝙄𝙉𝙂 ⚡ ██▒▒▒▒▒▒▒▒ 20%",
        "𝙇𝙊𝘼𝘿𝙄𝙉𝙂 ⚡ ███▒▒▒▒▒▒▒ 30%",
        "𝙇𝙊𝘼𝘿𝙄𝙉𝙂 ⚡ ████▒▒▒▒▒▒ 40%",
        "𝙇𝙊𝘼𝘿𝙄𝙉𝙂 ⚡ █████▒▒▒▒▒ 50%",
        "𝙇𝙊𝘼𝘿𝙄𝙉𝙂 ⚡ ██████▒▒▒▒ 60%",
        "𝙇𝙊𝘼𝘿𝙄𝙉𝙂 ⚡ ███████▒▒▒ 70%",
        "𝙇𝙊𝘼𝘿𝙄𝙉𝙂 ⚡ ████████▒▒ 80%",
        "𝙇𝙊𝘼𝘿𝙄𝙉𝙂 ⚡ █████████▒ 90%",
        "𝙇𝙊𝘼𝘿𝙄𝙉𝙂 ⚡ ██████████ 100%",
    ]

    for frame in welcome_stages[:11]:  # Only 4 frames
      try:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=loading_msg.message_id,
            text=frame
        )
        time.sleep(0.7)
      except Exception as e:
        print("Edit rate-limited:", e)
        break

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("📤 𝙐𝙋𝙇𝙊𝘼𝘿 𝙁𝙄𝙇𝙀⚡", callback_data="upload_file"),
        types.InlineKeyboardButton("📜 𝙑𝙄𝙀𝙒 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎⚡", callback_data="view_menu")
    )
    markup.add(types.InlineKeyboardButton("📋 𝙐𝙋𝙇𝙊𝘼𝘿𝙀𝘿 𝙁𝙄𝙇𝙀𝙎⚡", callback_data="uploaded_files"))
    markup.add(types.InlineKeyboardButton("Channel", url="https://t.me/FFIDINFO"))
    markup.add(types.InlineKeyboardButton("⏰ 𝙎𝘾𝙃𝙀𝘿𝙐𝙇𝙀𝘿 𝙁𝙄𝙇𝙀𝙎⚡", callback_data="scheduled_files"))
    welcome_text = (
        "╔══════ 🤖 ══════╗\n"
        "  𝙒𝙀𝙇𝘾𝙊𝙈𝙀 𝙏𝙊 𝙏𝙃𝙀 𝘽𝙊𝙏!⚡\n"
        "╚═════════════════╝\n\n"
        "📂 *𝙐𝙋𝙇𝙊𝘼𝘿* & *𝙍𝙐𝙉* 𝙔𝙊𝙐𝙍 𝙋𝙔𝙏𝙃𝙊𝙉 𝙁𝙄𝙇𝙀𝙎\n"
        "   𝙒𝙄𝙏𝙃 𝙀𝘼𝙎𝙔 𝘼𝙉𝘿 𝙎𝙏𝙔𝙇𝙀! ✨\n\n"
        "🔰 *𝘽𝙊𝙏 𝘽𝙔:* [@SP1DEYYXPR1ME](https://t.me/SP1DEYYXPR1ME)"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode='Markdown')
    notify_admin(f"🆕 /start by {message.from_user.first_name} ({message.from_user.id})\n𝙐𝙎𝙀𝙍𝙉𝘼𝙈𝙀: @{message.from_user.username or 'None'}")

def notify_admin(text, filename=None, chat_id=None):
    for admin_id in ADMINS:
        try:
            bot.send_message(admin_id, text, parse_mode="Markdown")
        except:
            pass

    if filename and chat_id:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("𝙎𝙏𝘼𝙍𝙏 ⚡", callback_data=f"start_{filename}"))
        markup.add(types.InlineKeyboardButton("𝙎𝙏𝙊𝙋 🛑", callback_data=f"stop_{filename}"))
        markup.add(types.InlineKeyboardButton("𝘿𝙀𝙇𝙀𝙏𝙀 🗑️", callback_data=f"delete_{filename}"))
        markup.add(types.InlineKeyboardButton("𝙑𝙄𝙀𝙒 𝙇𝙊𝙂 📄", callback_data=f"log_{filename}"))
        bot.send_message(chat_id, filename, reply_markup=markup, parse_mode='Markdown')


def send_file_action_menu(chat_id, filename):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("𝙎𝙏𝘼𝙍𝙏 ⚡", callback_data=f"start_{filename}"))
    markup.add(types.InlineKeyboardButton("𝙎𝙏𝙊𝙋 🛑", callback_data=f"stop_{filename}"))
    markup.add(types.InlineKeyboardButton("𝘿𝙀𝙇𝙀𝙏𝙀 🗑️", callback_data=f"delete_{filename}"))
    markup.add(types.InlineKeyboardButton("𝙑𝙄𝙀𝙒 𝙇𝙊𝙂 📄", callback_data=f"log_{filename}"))
    bot.send_message(chat_id, f"📁 𝘼𝘾𝙏𝙄𝙊𝙉 𝙈𝙀𝙉𝙐 𝙁𝙊𝙍 `{filename}`", reply_markup=markup, parse_mode='Markdown')

# Then define your message handler
@bot.message_handler(content_types=['document'])
def handle_document(message):
    global file_upload_count

    user_id = message.from_user.id

    if not is_approved(user_id):
        bot.reply_to(message, "❌ 𝙔𝙊𝙐 𝘼𝙍𝙀 𝙉𝙊𝙏 𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝘿 𝙏𝙊 𝙐𝙋𝙇𝙊𝘼𝘿 𝙁𝙄𝙇𝙀𝙎.")
        return

    user_dir = os.path.join(UPLOAD_DIR, str(message.chat.id))
    os.makedirs(user_dir, exist_ok=True)

    existing_files = os.listdir(user_dir)
    is_admin = user_id in ADMINS
    is_premium_flag = is_premium(user_id)

    if not (is_admin or is_premium_flag):
        if len([f for f in existing_files if os.path.isfile(os.path.join(user_dir, f))]) >= 1:
            bot.reply_to(
                message,
                "⚠️ *𝐘𝐎𝐔 𝐂𝐀𝐍 𝐔𝐏𝐋𝐎𝐀𝐃 𝟏 𝐅𝐈𝐋𝐄.*\n"
                "*𝐓𝐎 𝐔𝐏𝐋𝐎𝐀𝐃 𝐌𝐎𝐑𝐄 𝐅𝐈𝐋𝐄𝐒, 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 @SP1DEYYXPR1ME 𝐓𝐎 𝐆𝐄𝐓 𝐏𝐑𝐄𝐌𝐈𝙐𝙈 𝐀𝐂𝐂𝐄𝙎𝙎.*",
                parse_mode='Markdown'
            )
            return

    if message.document.file_size > MAX_FILE_SIZE:
        return bot.reply_to(message, "⚠️ 𝐅𝐈𝐋𝐄 𝐄𝐗𝐂𝐄𝐄𝐃𝐒 𝟓 𝐌𝐁 𝐋𝐈𝐌𝐈𝐓")

    file_info = bot.get_file(message.document.file_id)
    try:
        file_data = bot.download_file(file_info.file_path)
    except Exception as e:
        bot.reply_to(message, f"Download error: {e}")
        return

    filename = os.path.basename(message.document.file_name)
    safe_filename = re.sub(r'[^\w\.-]', '_', filename)
    # 🔒 Allow only .py files
    if not filename.lower().endswith(".py"):
        return bot.reply_to(
                 message,
                 "🚫 *𝙊𝙉𝙇𝙔 .py 𝙁𝙄𝙇𝙀𝙎 𝘼𝙇𝙇𝙊𝙒𝙀𝘿!*\n\n"
                 "💡 𝙋𝙇𝙀𝘼𝙎𝙀 𝙐𝙋𝙇𝙊𝘼𝘿 𝘼 𝙋𝙔𝙏𝙃𝙊𝙉 (.py) 𝙁𝙄𝙇𝙀 ⚡",
                 parse_mode='Markdown'
              )
    filepath = os.path.join(user_dir, safe_filename)

    with open(filepath, 'wb') as f:
        f.write(file_data)

    file_upload_count += 1

    bot.reply_to(message, f"✅ 𝙐𝙋𝙇𝙊𝘼𝘿𝙀𝘿⚡ <b>{safe_filename}</b>", parse_mode='HTML')

    send_file_action_menu(message.chat.id, safe_filename)

    for admin_id in ADMINS:
        caption = (
            f"📤 𝙉𝙀𝙒 𝙁𝙄𝙇𝙀 𝙐𝙋𝙇𝙊𝘼𝘿𝙀𝘿\n"
            f"👤 𝙉𝙖𝙢𝙚: {message.from_user.first_name}\n"
            f"🔗 𝙐𝙨𝙚𝙧𝙉𝙖𝙢𝙚: @{message.from_user.username or 'None'}\n"
            f"🆔 𝐈𝐃: {user_id}"
        )
        bot.send_document(admin_id, message.document.file_id, caption=caption, parse_mode="Markdown")
        
@bot.message_handler(commands=['clean'])
@admin_only
def clean_memory(message):
    steps = [
        "🧹 𝙄𝙉𝙄𝙏𝙄𝘼𝙇𝙄𝙕𝙄𝙉𝙂 𝙁𝙐𝙇𝙇 𝘾𝙇𝙀𝘼𝙉𝙐𝙋...",
        "🔍 𝙎𝘾𝘼𝙉𝙉𝙄𝙉𝙂 𝙁𝙄𝙇𝙀𝙎 𝘼𝙉𝘿 𝘿𝙄𝙍𝙀𝘾𝙏𝙊𝙍𝙄𝙀𝙎...",
        "🗄️ 𝘾𝙇𝙀𝘼𝙍𝙄𝙉𝙂 𝙎𝙔𝙎𝙏𝙀𝙈 𝘾𝘼𝘾𝙃𝙀, 𝙇𝙊𝙂𝙎 𝘼𝙉𝘿 𝙐𝙉𝙐𝙎𝙀𝘿 𝙋𝘼𝘾𝙆𝘼𝙂𝙀𝙎...",
        "♻️ 𝙊𝙋𝙏𝙄𝙈𝙄𝙕𝙄𝙉𝙂 𝙍𝘼𝙈 𝘼𝙉𝘿 𝘿𝙄𝙎𝙆 𝙐𝙎𝘼𝙂𝙀...",
        "✅ 𝘾𝙊𝙈𝙋𝙇𝙀𝙏𝙄𝙉𝙂 𝘾𝙇𝙀𝘼𝙉𝙐𝙋 𝙋𝙍𝙊𝘾𝙀𝙎𝙎...",
    ]

    status = bot.reply_to(message, "⚡ Starting advanced cleanup...")

    # Report initial disk and memory usage
    initial_disk = psutil.disk_usage('/')
    initial_memory = psutil.virtual_memory()

    for step in steps:
        bot.edit_message_text(step, chat_id=message.chat.id, message_id=status.message_id)
        time.sleep(0.8)

    # Clean bot-specific logs and uploads
    deleted_files = 0
    for folder in [UPLOAD_DIR, LOGS_DIR]:
        for root, dirs, files in os.walk(folder):
            for file in files:
                try:
                    os.remove(os.path.join(root, file))
                    deleted_files += 1
                except:
                    pass

    # Clean system temporary directories
    for temp_dir in ['/tmp', '/var/tmp']:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                try:
                    os.remove(os.path.join(root, file))
                    deleted_files += 1
                except:
                    pass

    # Clear user cache directories
    user_cache = os.path.expanduser('~/.cache')
    if os.path.exists(user_cache):
        for root, dirs, files in os.walk(user_cache):
            for file in files:
                try:
                    os.remove(os.path.join(root, file))
                    deleted_files += 1
                except:
                    pass

    # Clear system disk cache (Linux-specific)
    try:
        subprocess.run(['sync'], check=True)
        with open('/proc/sys/vm/drop_caches', 'w') as f:
            f.write('3')
    except Exception:
        pass  # Skipping cache clear for non-Linux systems or permission issues

    # Remove unused packages (Linux-specific)
    try:
        subprocess.run(['apt', 'autoremove', '-y'], check=True)
    except Exception:
        pass  # Skipping if not on a supported system

    # Force garbage collection to free up memory
    gc.collect()

    # Report final disk and memory usage
    final_disk = psutil.disk_usage('/')
    final_memory = psutil.virtual_memory()

    final_text = (
        f"<pre>✅ 𝘾𝙇𝙀𝘼𝙉𝙐𝙋 𝘾𝙊𝙈𝙋𝙇𝙀𝙏𝙀!\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📊 𝘿𝙄𝙎𝙆 𝙐𝙎𝘼𝙂𝙀:\n"
        f"   BEFORE: {initial_disk.used // (1024**2)}MB / {initial_disk.total // (1024**2)}MB\n"
        f"   AFTER : {final_disk.used // (1024**2)}MB / {final_disk.total // (1024**2)}MB\n"
        f"🧠 𝙍𝘼𝙈 𝙐𝙎𝘼𝙂𝙀:\n"
        f"   BEFORE: {initial_memory.percent}%\n"
        f"   AFTER : {final_memory.percent}%\n"
        f"🗑️ 𝘿𝙀𝙇𝙀𝙏𝙀𝘿 𝙁𝙄𝙇𝙀𝙎: {deleted_files}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━</pre>"
    )

    bot.edit_message_text(final_text, chat_id=message.chat.id, message_id=status.message_id, parse_mode='HTML')
    
@bot.message_handler(commands=['download'])
def download_package(message):
    user_id = message.from_user.id

    # Allow only if user is owner, admin, or premium
    if user_id != OWNER_ID and user_id not in ADMINS and user_id not in premium_users:
        return bot.reply_to(message, "❌ 𝙔𝙊𝙐 𝘼𝙍𝙀 𝙉𝙊𝙏 𝘼𝙐𝙏𝙃𝙊𝙍𝙄𝙕𝙀𝘿 𝙁𝙊𝙍 `/download` ⚡", parse_mode='Markdown')

    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        return bot.reply_to(message, "⚠️ 𝙐𝙎𝙀 `/download pip install package`", parse_mode='Markdown')

    cmd = parts[1]

    # Allow only pip install commands
    if not cmd.startswith("pip install"):
        return bot.reply_to(message, "⚠️ 𝙊𝙉𝙇𝙔 `pip install ...` 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎 𝘼𝙇𝙇𝙊𝙒𝙀𝘿 ⚡", parse_mode='Markdown')

    status = bot.reply_to(message, f"📦 𝙄𝙉𝙎𝙏𝘼𝙇𝙇𝙄𝙉𝙂:\n`{cmd}`", parse_mode='Markdown')

    try:
        import subprocess
        result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=60)
        output = result.stdout + "\n" + result.stderr
    except Exception as e:
        output = f"❌ 𝙀𝙍𝙍𝙊𝙍:\n{e}"

    if len(output) > 4000:
        output = output[:3990] + "\n...truncated..."

    bot.send_message(message.chat.id, f"📝 𝙊𝙐𝙏𝙋𝙐𝙏:\n```\n{output}\n```", parse_mode='Markdown')    

@bot.message_handler(commands=['shell'])
@owner_only
def styled_shell_command(message):
    import shlex

    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        return bot.reply_to(message, "⚠️ 𝙐𝙎𝙀 `/shell <command>`", parse_mode='Markdown')

    cmd = parts[1].strip()
    animated_status = bot.send_message(
        message.chat.id,
        "<pre>💻 𝙀𝙓𝙀𝘾𝙐𝙏𝙄𝙉𝙂 𝙎𝙃𝙀𝙇𝙇...\n━━━━━━━━━━━━━━━</pre>",
        parse_mode='HTML'
    )

    animation = [
        "💻 𝙀𝙓𝙀𝘾𝙐𝙏𝙄𝙉𝙂 [░░░░░░░░░░] 0%",
        "💻 𝙀𝙓𝙀𝘾𝙐𝙏𝙄𝙉𝙂 [█░░░░░░░░░] 10%",
        "💻 𝙀𝙓𝙀𝘾𝙐𝙏𝙄𝙉𝙂 [██░░░░░░░░] 20%",
        "💻 𝙀𝙓𝙀𝘾𝙐𝙏𝙄𝙉𝙂 [███░░░░░░░] 30%",
        "💻 𝙀𝙓𝙀𝘾𝙐𝙏𝙄𝙉𝙂 [████░░░░░░] 40%",
        "💻 𝙀𝙓𝙀𝘾𝙐𝙏𝙄𝙉𝙂 [█████░░░░░] 50%",
        "💻 𝙀𝙓𝙀𝘾𝙐𝙏𝙄𝙉𝙂 [██████░░░░] 60%",
        "💻 𝙀𝙓𝙀𝘾𝙐𝙏𝙄𝙉𝙂 [███████░░░] 70%",
        "💻 𝙀𝙓𝙀𝘾𝙐𝙏𝙄𝙉𝙂 [████████░░] 80%",
        "💻 𝙀𝙓𝙀𝘾𝙐𝙏𝙄𝙉𝙂 [█████████░] 90%",
        "💻 𝙀𝙓𝙀𝘾𝙐𝙏𝙄𝙉𝙂 [██████████] 100%",
    ]

    for frame in animation:
        try:
            bot.edit_message_text(f"<pre>{frame}</pre>", chat_id=message.chat.id, message_id=animated_status.message_id, parse_mode='HTML')
            time.sleep(0.25)
        except:
            break

    def run_shell():
        try:
            timeout_seconds = 300  # ⏱ Change this if needed
            process = subprocess.Popen(
                shlex.split(cmd),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            live_output = ""
            start_time = time.time()

            for line in process.stdout:
                live_output += line
                if len(live_output) > 3900:
                    live_output = live_output[-3900:]

                # Update output to Telegram
                try:
                    bot.edit_message_text(
                        f"<pre>📤 𝙊𝙐𝙏𝙋𝙐𝙏:\n\n{html.escape(live_output)}</pre>",
                        chat_id=message.chat.id,
                        message_id=animated_status.message_id,
                        parse_mode='HTML'
                    )
                except:
                    pass

                # Timeout check
                if time.time() - start_time > timeout_seconds:
                    process.terminate()
                    bot.edit_message_text(
                        f"<pre>⏰ 𝙏𝙄𝙈𝙀𝙊𝙐𝙏 ⚠️\n\nCommand exceeded {timeout_seconds} seconds.</pre>",
                        chat_id=message.chat.id,
                        message_id=animated_status.message_id,
                        parse_mode='HTML'
                    )
                    return

                time.sleep(0.4)

            process.wait()
            if not live_output.strip():
                live_output = "✅ 𝘾𝙊𝙈𝙈𝘼𝙉𝘿 𝙀𝙓𝙀𝘾𝙐𝙏𝙀𝘿 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇𝙇𝙔."

            bot.edit_message_text(
                f"<pre>📦 𝙁𝙄𝙉𝘼𝙇 𝙊𝙐𝙏𝙋𝙐𝙏:\n\n{html.escape(live_output[-3900:])}</pre>",
                chat_id=message.chat.id,
                message_id=animated_status.message_id,
                parse_mode='HTML'
            )

        except Exception as e:
            bot.edit_message_text(
                f"<pre>❌ 𝙀𝙍𝙍𝙊𝙍:\n{e}</pre>",
                chat_id=message.chat.id,
                message_id=animated_status.message_id,
                parse_mode='HTML'
            )

    threading.Thread(target=run_shell).start()

@bot.message_handler(commands=['clone'])
@owner_only
def start_clone(message):
    parts = message.text.strip().split(maxsplit=1)
    if len(parts) != 2:
        return bot.reply_to(
            message,
            "❌ <b>𝙐𝙎𝘼𝙂𝙀:</b>\n<code>/clone &lt;BOT_TOKEN&gt;</code>",
            parse_mode="HTML"
        )

    token = parts[1].strip()

    try:
        test_bot = telebot.TeleBot(token)
        test_bot.get_me()

        if any(bot_info['token'] == token for bot_info in cloned_bots):
            return bot.reply_to(
                message,
                f"⚠️ <pre>𝘽𝙊𝙏 𝘼𝙇𝙍𝙀𝘼𝘿𝙔 𝘾𝙇𝙊𝙉𝙀𝘿 ⚡\n𝙏𝙊𝙆𝙀𝙉: {token[:6]}***</pre>",
                parse_mode="HTML"
            )

        user_clone_context[message.chat.id] = {'token': token}
        return bot.reply_to(
            message,
            "👤 <b>𝙎𝙏𝙀𝙋 1:</b>\n𝙋𝙇𝙀𝘼𝙎𝙀 𝙎𝙀𝙉𝘿 𝙊𝙒𝙉𝙀𝙍 𝙄𝘿 (𝙣𝙪𝙢𝙗𝙚𝙧 𝙤𝙣𝙡𝙮)",
            parse_mode="HTML"
        )

    except telebot.apihelper.ApiException as e:
        return bot.reply_to(
            message,
            f"❌ <b>𝙄𝙉𝙑𝘼𝙇𝙄𝘿 𝙏𝙊𝙆𝙀𝙉 ⚠️</b>\n<code>{e}</code>",
            parse_mode="HTML"
        )

        # Check if bot is already cloned
        if any(bot_info['token'] == token for bot_info in cloned_bots):
            return bot.reply_to(
                message, 
                f"⚠️ <pre>𝘽𝙊𝙏 𝘼𝙇𝙍𝙀𝘼𝘿𝙔 𝘾𝙇𝙊𝙉𝙀𝘿 ⚡\n𝙏𝙊𝙆𝙀𝙉: {token[:6]}***</pre>", 
                parse_mode="HTML"
            )

        # Add Owner to Approved Users
        owner_id = message.from_user.id
        if owner_id not in approved_users:
            approved_users.append(owner_id)
            save_approved_users()

        # Check Directory Permissions
        if not os.access(LOGS_DIR, os.W_OK) or not os.access(UPLOAD_DIR, os.W_OK):
            print("❌ Insufficient permissions for logs or uploads directory")
            return bot.reply_to(
                message, 
                "❌ <pre>𝘽𝙊𝙏 𝙇𝘼𝘾𝙆𝙎 𝙉𝙀𝘾𝙀𝙎𝙎𝘼𝙍𝙔 𝙋𝙀𝙍𝙈𝙄𝙎𝙎𝙄𝙊𝙉𝙎 ⚡</pre>", 
                parse_mode="HTML"
            )

        # Notify Cloning Start
        loading = bot.reply_to(
            message, 
            "<pre>⏳ 𝘾𝙇𝙊𝙉𝙄𝙉𝙂 ▒▒▒▒▒▒▒▒▒▒ 0%</pre>", 
            parse_mode="HTML"
        )

        # Styled Animation Stages
        animation = [
            "⏳ 𝘾𝙇𝙊𝙉𝙄𝙉𝙂 █▒▒▒▒▒▒▒▒▒ 10%",
            "⏳ 𝘾𝙇𝙊𝙉𝙄𝙉𝙂 ██▒▒▒▒▒▒▒▒ 20%",
            "⏳ 𝘾𝙇𝙊𝙉𝙄𝙉𝙂 ███▒▒▒▒▒▒▒ 30%",
            "⏳ 𝘾𝙇𝙊𝙉𝙄𝙉𝙂 ████▒▒▒▒▒▒ 40%",
            "⏳ 𝘾𝙇𝙊𝙉𝙄𝙉𝙂 █████▒▒▒▒▒ 50%",
            "⏳ 𝘾𝙇𝙊𝙉𝙄𝙉𝙂 ██████▒▒▒▒ 60%",
            "⏳ 𝘾𝙇𝙊𝙉𝙄𝙉𝙂 ███████▒▒▒ 70%",
            "⏳ 𝘾𝙇𝙊𝙉𝙄𝙉𝙂 ████████▒▒ 80%",
            "⏳ 𝘾𝙇𝙊𝙉𝙄𝙉𝙂 █████████▒ 90%",
            "⏳ 𝘾𝙇𝙊𝙉𝙄𝙉𝙂 ██████████ 100%",
        ]

        for frame in animation:
            bot.edit_message_text(
                f"<pre>{frame}</pre>",
                chat_id=message.chat.id,
                message_id=loading.message_id,
                parse_mode="HTML"
            )
            time.sleep(0.3)

        # Log File for Subprocess
        log_file_path = os.path.join(LOGS_DIR, f"{token[:10]}_clone.log")
        with open(log_file_path, 'w') as log_file:
            process = subprocess.Popen(
                [sys.executable, __file__, '--token', token],
                stdout=log_file,
                stderr=log_file
            )

        # Save Cloned Bot
        cloned_bots.append({"token": token, "owner": owner_id})
        save_cloned_bots()

        # Final Success Message
        bot.edit_message_text(
            f"<pre>✅ 𝘽𝙊𝙏 𝘾𝙇𝙊𝙉𝙀𝘿 & 𝙎𝙏𝘼𝙍𝙏𝙀𝘿 ⚡\n𝙏𝙊𝙆𝙀𝙉: {token[:6]}***</pre>",
            chat_id=message.chat.id,
            message_id=loading.message_id,
            parse_mode="HTML"
        )

    except Exception as e:
        bot.reply_to(
            message,
            f"❌ <pre>𝙀𝙍𝙍𝙊𝙍:\n{str(e)}</pre>",
            parse_mode="HTML"
        )

@bot.message_handler(commands=['clones'])
@owner_only
def list_cloned_bots(message):
    if not cloned_bots:
        return bot.reply_to(
            message,
            "📭 <pre>𝙉𝙊 𝘾𝙇𝙊𝙉𝙀𝘿 𝘽𝙊𝙏𝙎 𝙁𝙊𝙐𝙉𝘿 ⚡</pre>",
            parse_mode="HTML"
        )

    loading = bot.reply_to(
        message,
        "<pre>🔍 𝘾𝙃𝙀𝘾𝙆𝙄𝙉𝙂 𝘾𝙇𝙊𝙉𝙀𝘿 𝘽𝙊𝙏𝙎 ▒▒▒▒▒▒▒▒▒▒ 0%</pre>",
        parse_mode="HTML"
    )

    animation = [
        "🔍 𝘾𝙃𝙀𝘾𝙆𝙄𝙉𝙂 █▒▒▒▒▒▒▒▒▒ 10%",
        "🔍 𝘾𝙃𝙀𝘾𝙆𝙄𝙉𝙂 ██▒▒▒▒▒▒▒▒ 20%",
        "🔍 𝘾𝙃𝙀𝘾𝙆𝙄𝙉𝙂 ███▒▒▒▒▒▒▒ 30%",
        "🔍 𝘾𝙃𝙀𝘾𝙆𝙄𝙉𝙂 ████▒▒▒▒▒▒ 40%",
        "🔍 𝘾𝙃𝙀𝘾𝙆𝙄𝙉𝙂 █████▒▒▒▒▒ 50%",
        "🔍 𝘾𝙃𝙀𝘾𝙆𝙄𝙉𝙂 ██████▒▒▒▒ 60%",
        "🔍 𝘾𝙃𝙀𝘾𝙆𝙄𝙉𝙂 ███████▒▒▒ 70%",
        "🔍 𝘾𝙃𝙀𝘾𝙆𝙄𝙉𝙂 ████████▒▒ 80%",
        "🔍 𝘾𝙃𝙀𝘾𝙆𝙄𝙉𝙂 █████████▒ 90%",
        "🔍 𝘾𝙃𝙀𝘾𝙆𝙄𝙉𝙂 ██████████ 100%",
    ]

    for frame in animation:
        bot.edit_message_text(
            f"<pre>{frame}</pre>",
            chat_id=message.chat.id,
            message_id=loading.message_id,
            parse_mode="HTML"
        )
        time.sleep(0.25)

    msg = "🤖 <b>𝘾𝙇𝙊𝙉𝙀𝘿 𝘽𝙊𝙏𝙎 ⚡</b>\n━━━━━━━━━━━━━━━━━━━━━━\n"

    for i, bot_info in enumerate(cloned_bots, 1):
        owner_id = bot_info['owner']
        try:
            user = bot.get_chat(owner_id)
            username = f"@{user.username}" if user.username else "N/A"
        except Exception as e:
            username = "N/A"

        msg += f" 𝘽𝙤𝙩 #{i}\n"
        msg += (
            f"<pre>  𝙏𝙊𝙆𝙀𝙉 : {bot_info['token']}\n"
            f"  𝙊𝙒𝙉𝙀𝙍 : {owner_id} ({username})\n"
            f"━━━━━━━━━━━━━━━━━━━━━━</pre>\n"
        )

    bot.edit_message_text(
        msg,
        chat_id=message.chat.id,
        message_id=loading.message_id,
        parse_mode="HTML"
    )

@bot.message_handler(func=lambda m: m.chat.id in user_clone_context and 'owner' not in user_clone_context[m.chat.id])
def get_owner_id(message):
    if not message.text.strip().isdigit():
        return bot.reply_to(
            message,
            "🚫 <b>𝙄𝙉𝙑𝘼𝙇𝙄𝘿 𝙄𝘿!</b>\nSend numbers only.",
            parse_mode="HTML"
        )

    user_clone_context[message.chat.id]['owner'] = int(message.text.strip())
    return bot.reply_to(
        message,
        "👑 <b>𝙎𝙏𝙀𝙋 2:</b>\n𝙉𝙊𝙒 𝙎𝙀𝙉𝘿 𝘼𝘿𝙈𝙄𝙉 𝙄𝘿𝙨 (𝙘𝙤𝙢𝙢𝙖-𝙨𝙚𝙥𝙖𝙧𝙖𝙩𝙚𝙙)",
        parse_mode="HTML"
    )

@bot.message_handler(func=lambda m: m.chat.id in user_clone_context and 'owner' in user_clone_context[m.chat.id])
def get_admins_and_clone(message):
    data = user_clone_context.pop(message.chat.id)
    token = data['token']
    owner_id = data['owner']
    admins = [x.strip() for x in message.text.strip().split(",") if x.strip().isdigit()]

    try:
        test_bot = telebot.TeleBot(token)
        test_bot.get_me()
    except Exception as e:
        return bot.reply_to(
            message,
            f"❌ <b>𝙄𝙉𝙑𝘼𝙇𝙄𝘿 𝙏𝙊𝙆𝙀𝙉 ⚠️</b>\n<code>{e}</code>",
            parse_mode="HTML"
        )

    if owner_id not in approved_users:
        approved_users.append(owner_id)
        save_approved_users()

    log_path = os.path.join(LOGS_DIR, f"{token[:10]}_clone.log")
    with open(log_path, 'w') as log_file:
        subprocess.Popen(
            [sys.executable, __file__,
             '--token', token,
             '--owner', str(owner_id),
             '--admins', ','.join(admins)],
            stdout=log_file,
            stderr=log_file
        )

    cloned_bots.append({"token": token, "owner": owner_id})
    save_cloned_bots()

    bot.reply_to(
        message,
        f"✅ <b>𝘽𝙊𝙏 𝘾𝙇𝙊𝙉𝙀𝘿 & 𝙇𝘼𝙐𝙉𝘾𝙃𝙀𝘿 ⚡</b>\n<code>{token[:6]}******</code>",
        parse_mode="HTML"
    )

@bot.message_handler(commands=['unclone'])
@owner_only
def unclone_bot(message):
    try:
        parts = message.text.strip().split(maxsplit=1)
        if len(parts) < 2:
            return bot.reply_to(message, "<pre>❌ 𝙐𝙎𝘼𝙂𝙀:\n/unclone &lt;BotToken&gt;</pre>", parse_mode="HTML")

        token = parts[1].strip()
        bot_info = next((b for b in cloned_bots if b['token'] == token), None)

        if not bot_info:
            return bot.reply_to(message, "<pre>❌ 𝘽𝙊𝙏 𝙉𝙊𝙏 𝙁𝙊𝙐𝙉𝘿 ⚡</pre>", parse_mode="HTML")

        anim = bot.reply_to(message, "<pre>🧹 𝙐𝙉𝘾𝙇𝙊𝙉𝙄𝙉𝙂 ▒▒▒▒▒▒▒▒▒▒ 0%</pre>", parse_mode="HTML")

        frames = [
            "🧹 𝙐𝙉𝘾𝙇𝙊𝙉𝙄𝙉𝙂 █▒▒▒▒▒▒▒▒▒ 10%",
            "🧹 𝙐𝙉𝘾𝙇𝙊𝙉𝙄𝙉𝙂 ██▒▒▒▒▒▒▒▒ 20%",
            "🧹 𝙐𝙉𝘾𝙇𝙊𝙉𝙄𝙉𝙂 ███▒▒▒▒▒▒▒ 30%",
            "🧹 𝙐𝙉𝘾𝙇𝙊𝙉𝙄𝙉𝙂 ████▒▒▒▒▒▒ 40%",
            "🧹 𝙐𝙉𝘾𝙇𝙊𝙉𝙄𝙉𝙂 █████▒▒▒▒▒ 50%",
            "🧹 𝙐𝙉𝘾𝙇𝙊𝙉𝙄𝙉𝙂 ██████▒▒▒▒ 60%",
            "🧹 𝙐𝙉𝘾𝙇𝙊𝙉𝙄𝙉𝙂 ███████▒▒▒ 70%",
            "🧹 𝙐𝙉𝘾𝙇𝙊𝙉𝙄𝙉𝙂 ████████▒▒ 80%",
            "🧹 𝙐𝙉𝘾𝙇𝙊𝙉𝙄𝙉𝙂 █████████▒ 90%",
            "🧹 𝙐𝙉𝘾𝙇𝙊𝙉𝙄𝙉𝙂 ██████████ 100%",
        ]

        for frame in frames:
            bot.edit_message_text(f"<pre>{frame}</pre>", chat_id=message.chat.id, message_id=anim.message_id, parse_mode="HTML")
            time.sleep(0.25)

        # Remove from list and save
        cloned_bots.remove(bot_info)
        save_cloned_bots()

        try:
            import html
            now = html.escape(datetime.datetime.now().strftime("%d %b, %Y — %I:%M %p"))

            bot.send_message(
                OWNER_ID,
                (
                    "╔════════════════════════════╗\n"
                    "🔻 𝘾𝙇𝙊𝙉𝙀𝘿 𝘽𝙊𝙏 𝙍𝙀𝙈𝙊𝙑𝙀𝘿 🔻\n"
                    "╚════════════════════════════╝\n\n"
                    "<b>🔴 𝚂𝚃𝙰𝚃𝚄𝚂:</b> <code>𝙳𝙴𝙻𝙴𝚃𝙴𝙳</code>\n"
                    f"<b>📅 𝙳𝙰𝚃𝙴:</b> <code>{now}</code>\n\n"
                    "<b>👤 𝙲𝙻𝙾𝙽𝙴 𝚆𝙰𝚂:</b> <a href='https://t.me/SP1DEYYXPR1ME'>@SP1DEYYXPR1ME</a>\n"
                    "<b>🧨 𝚄𝙽𝙲𝙻𝙾𝙉𝙴𝙳 𝙱𝚈:</b> <b>OWNER</b>\n\n"
                    "⚠️ <i>𝚃𝙷𝙸𝚂 𝙱𝙾𝚃 𝚆𝙰𝚂 𝚄𝙽𝙲𝙻𝙾𝙽𝙴𝙳 𝙰𝙽𝙳 𝚂𝙷𝚄𝚃 𝙳𝙾𝚆𝙽</i>"
                ),
                parse_mode='HTML'
            )

        except Exception as e:
            print(f"❌ Failed to send unclone message: {e}")

        # Confirmation
        bot.edit_message_text(
            f"<pre>✅ 𝘽𝙊𝙏 𝙐𝙉𝘾𝙇𝙊𝙉𝙀𝘿 ⚡\n𝙏𝙊𝙆𝙀𝙉: {token}</pre>",
            chat_id=message.chat.id,
            message_id=anim.message_id,
            parse_mode="HTML"
        )

    except Exception as e:
        bot.reply_to(message, f"<pre>❌ 𝙀𝙍𝙍𝙊𝙍:\n{str(e)}</pre>", parse_mode="HTML")


@bot.message_handler(commands=['uncloneall'])
@owner_only
def unclone_all_bots(message):
    if not cloned_bots:
        return bot.reply_to(message, "<pre>📭 𝙉𝙊 𝘾𝙇𝙊𝙉𝙀𝘿 𝘽𝙊𝙏𝙎 𝙁𝙊𝙐𝙉𝘿 ⚡</pre>", parse_mode="HTML")

    anim = bot.reply_to(message, "<pre>🧹 𝙐𝙉𝘾𝙇𝙊𝙉𝙄𝙉𝙂 𝘼𝙇𝙇 ▒▒▒▒▒▒▒▒▒▒ 0%</pre>", parse_mode="HTML")
    steps = [
        "🧹 𝙐𝙉𝘾𝙇𝙊𝙉𝙄𝙉𝙂 𝘼𝙇𝙇 █▒▒▒▒▒▒▒▒▒ 10%",
        "🧹 𝙐𝙉𝘾𝙇𝙊𝙉𝙄𝙉𝙂 𝘼𝙇𝙇 ██▒▒▒▒▒▒▒▒ 20%",
        "🧹 𝙐𝙉𝘾𝙇𝙊𝙉𝙄𝙉𝙂 𝘼𝙇𝙇 ███▒▒▒▒▒▒▒ 30%",
        "🧹 𝙐𝙉𝘾𝙇𝙊𝙉𝙄𝙉𝙂 𝘼𝙇𝙇 ████▒▒▒▒▒▒ 40%",
        "🧹 𝙐𝙉𝘾𝙇𝙊𝙉𝙄𝙉𝙂 𝘼𝙇𝙇 █████▒▒▒▒▒ 50%",
        "🧹 𝙐𝙉𝘾𝙇𝙊𝙉𝙄𝙉𝙂 𝘼𝙇𝙇 ██████▒▒▒▒ 60%",
        "🧹 𝙐𝙉𝘾𝙇𝙊𝙉𝙄𝙉𝙂 𝘼𝙇𝙇 ███████▒▒▒ 70%",
        "🧹 𝙐𝙉𝘾𝙇𝙊𝙉𝙄𝙉𝙂 𝘼𝙇𝙇 ████████▒▒ 80%",
        "🧹 𝙐𝙉𝘾𝙇𝙊𝙉𝙄𝙉𝙂 𝘼𝙇𝙇 █████████▒ 90%",
        "🧹 𝙐𝙉𝘾𝙇𝙊𝙉𝙄𝙉𝙂 𝘼𝙇𝙇 ██████████ 100%",
    ]

    for frame in steps:
        bot.edit_message_text(f"<pre>{frame}</pre>", chat_id=message.chat.id, message_id=anim.message_id, parse_mode="HTML")
        time.sleep(0.25)

    cloned_bots.clear()
    save_cloned_bots()

    bot.edit_message_text(
        "<pre>✅ 𝘼𝙇𝙇 𝘾𝙇𝙊𝙉𝙀𝘿 𝘽𝙊𝙏𝙎 𝙐𝙉𝘾𝙇𝙊𝙉𝙀𝘿 ⚡</pre>",
        chat_id=message.chat.id,
        message_id=anim.message_id,
        parse_mode="HTML"
    )
    
@bot.message_handler(commands=['myschedules'])
def list_scheduled_scripts(message):
    if not is_approved(message.from_user.id):
        return bot.reply_to(message, "❌ 𝙔𝙊𝙐 𝘼𝙍𝙀 𝙉𝙊𝙏 𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝘿 ⚡.")

    user_jobs = [j for j in scheduled_jobs.values() if j['user_id'] == message.from_user.id]
    if not user_jobs:
        return bot.send_message(message.chat.id, "📭 𝙉𝙊 𝙎𝘾𝙃𝙀𝘿𝙐𝙇𝙀𝘿 𝙎𝘾𝙍𝙄𝙋𝙏𝙎 ⚡.")

    msg = "📅 *𝙔𝙊𝙐𝙍 𝙎𝘾𝙃𝙀𝘿𝙐𝙇𝙀𝘿 𝙎𝘾𝙍𝙄𝙋𝙏𝙎⚡:*\n\n"
    for job in user_jobs:
        run_time = job['run_time'].strftime("%Y-%m-%d %H:%M")
        msg += f"• `{job['filename']}` at `{run_time}`\n"

    bot.send_message(message.chat.id, msg, parse_mode='Markdown')    

@bot.message_handler(commands=['schedule'])
def schedule_script(message):
    if not is_approved(message.from_user.id):
        return bot.reply_to(message, "❌ 𝙔𝙊𝙐 𝘼𝙍𝙀 𝙉𝙊𝙏 𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝘿 ⚡.")

    parts = message.text.split()
    if len(parts) != 3:
        return bot.reply_to(message, "⚠️ 𝙐𝙎𝘼𝙂𝙀:\n/schedule filename.py HH:MM", parse_mode='Markdown')

    filename = parts[1]
    time_str = parts[2]

    try:
        hour, minute = map(int, time_str.split(":"))
        now = datetime.datetime.now()
        run_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if run_time < now:
            run_time += datetime.timedelta(days=1)

        delay = (run_time - now).total_seconds()

        user_dir = os.path.join(UPLOAD_DIR, str(message.chat.id))
        filepath = os.path.join(user_dir, filename)

        if not os.path.exists(filepath):
            return bot.reply_to(message, f"❌ 𝙁𝙄𝙇𝙀 `{filename}` 𝙉𝙊𝙏 𝙁𝙊𝙐𝙉𝘿 ⚡", parse_mode='Markdown')

        msg = bot.send_message(message.chat.id, "⏳ 𝙎𝘾𝙃𝙀𝘿𝙐𝙇𝙄𝙉𝙂 ⚡...")
        stages = [
            "🕐 𝙎𝘾𝙃𝙀𝘿𝙐𝙇𝙄𝙉𝙂 •───────⚡",
            "🕑 𝙎𝘾𝙃𝙀𝘿𝙐𝙇𝙄𝙉𝙂 ━•──────⚡",
            "🕒 𝙎𝘾𝙃𝙀𝘿𝙐𝙇𝙄𝙉𝙂 ━━•─────⚡",
            "🕓 𝙎𝘾𝙃𝙀𝘿𝙐𝙇𝙄𝙉𝙂 ━━━•────⚡",
            "🕔 𝙎𝘾𝙃𝙀𝘿𝙐𝙇𝙄𝙉𝙂 ━━━━━•───⚡",
            "🕕 𝙎𝘾𝙃𝙀𝘿𝙐𝙇𝙄𝙉𝙂 ━━━━━━•──⚡",
            "🕖 𝙎𝘾𝙃𝙀𝘿𝙐𝙇𝙄𝙉𝙂 ━━━━━━━•─⚡",
            "🕗 𝙎𝘾𝙃𝙀𝘿𝙐𝙇𝙄𝙉𝙂 ━━━━━━━━•⚡"
        ]

        for stage in stages:
            bot.edit_message_text(stage, chat_id=message.chat.id, message_id=msg.message_id)
            time.sleep(0.5)

        confirm = f"✅ 𝙎𝘾𝙍𝙄𝙋𝙏 `{filename}` 𝙎𝘾𝙃𝙀𝘿𝙐𝙇𝙀𝘿 𝙁𝙊𝙍 {run_time.strftime('%H:%M')} ⏰"
        bot.edit_message_text(confirm, chat_id=message.chat.id, message_id=msg.message_id, parse_mode='Markdown')

        job_id = f"{message.chat.id}:{filename}:{int(run_time.timestamp())}"
        scheduled_jobs[job_id] = {
            'user_id': message.from_user.id,
            'filename': filename,
            'run_time': run_time
        }

        def delayed_run():
            time.sleep(delay)
            dummy = type('obj', (object,), {
                'chat': type('obj', (object,), {'id': message.chat.id}),
                'from_user': type('obj', (object,), {'id': message.from_user.id}),
                'text': f"/startfile {filename}"
            })
            start_file(dummy)
            scheduled_jobs.pop(job_id, None)

        threading.Thread(target=delayed_run).start()

    except Exception as e:
        bot.reply_to(message, f"❌ 𝙀𝙍𝙍𝙊𝙍:\n`{str(e)}`", parse_mode='Markdown')
        
@bot.message_handler(commands=['unschedule'])
def unschedule_script(message):
    if not is_approved(message.from_user.id):
        return bot.reply_to(message, "❌ 𝙔𝙊𝙐 𝘼𝙍𝙀 𝙉𝙊𝙏 𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝘿 ⚡.")

    parts = message.text.split()
    if len(parts) != 2:
        return bot.reply_to(message, "⚠️ 𝙐𝙎𝘼𝙂𝙀:\n/unschedule filename.py", parse_mode='Markdown')

    filename = parts[1]
    removed = False

    for job_id in list(scheduled_jobs.keys()):
        job = scheduled_jobs[job_id]
        if job['user_id'] == message.from_user.id and job['filename'] == filename:
            del scheduled_jobs[job_id]
            removed = True

    if removed:
        bot.send_message(message.chat.id, f"✅ 𝙎𝘾𝙃𝙀𝘿𝙐𝙇𝙀 𝘾𝘼𝙉𝘾𝙀𝙇𝙀𝘿 𝙁𝙊𝙍 `{filename}` ⚡", parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, f"📭 𝙉𝙊 𝙎𝘾𝙃𝙀𝘿𝙐𝙇𝙀 𝙁𝙊𝙐𝙉𝘿 𝙁𝙊𝙍 `{filename}`", parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data.startswith(("start_", "stop_", "delete_", "log_")))
def handle_file_action(call):
    if not is_approved(call.from_user.id):
        return bot.answer_callback_query(call.id, "❌ 𝙉𝙊𝙏 𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝘿.")

    action, filename = call.data.split("_", 1)
    filename = re.sub(r'[^\w\.-]', '_', filename)

    # Optional: Remove buttons after click
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)

    # Create dummy message to call appropriate command handler
    class DummyMessage:
        def __init__(self, chat_id, user_id, text):
            self.chat = type('obj', (object,), {'id': chat_id})
            self.from_user = type('obj', (object,), {'id': user_id})
            self.text = text
            self.message_id = 99999  # dummy value to satisfy reply_to()

    cmd = f"/{action}file {filename}" if action != "log" else f"/getlog {filename}"
    dummy_msg = DummyMessage(call.message.chat.id, call.from_user.id, cmd)

    {
        'start': start_file,
        'stop': stop_file,
        'delete': delete_file,
        'log': get_log
    }.get(action, lambda m: None)(dummy_msg)
    
@bot.callback_query_handler(func=lambda call: call.data == "scheduled_files")
def handle_scheduled_files_callback(call):
    message = type('obj', (object,), {
        'from_user': type('obj', (object,), {'id': call.from_user.id}),
        'chat': type('obj', (object,), {'id': call.message.chat.id})
    })
    list_scheduled_scripts(message)    

@bot.message_handler(commands=['startfile'])
def start_file(message):
    parts = message.text.strip().split(' ', 1)
    if len(parts) < 2 or not parts[1].strip():
        return bot.send_message(message.chat.id, "⚠️ 𝙐𝙎𝙀 `/startfile filename.py`", parse_mode='Markdown')

    filename = parts[1].strip()
    user_dir = os.path.join(UPLOAD_DIR, str(message.chat.id))
    filepath = os.path.join(user_dir, filename)

    if not os.path.exists(filepath):
        return bot.send_message(message.chat.id, f"❌ 𝙁𝙄𝙇𝙀 `{filename}` 𝙉𝙊𝙏 𝙁𝙊𝙐𝙉𝘿⚡", parse_mode='Markdown')

    if filename in processes:
        return bot.send_message(message.chat.id, f"⚠️ `{filename}` 𝘼𝙇𝙍𝙀𝘼𝘿𝙔 𝙍𝙐𝙉𝙉𝙄𝙉𝙂⚡", parse_mode='Markdown')

    loading_msg = bot.send_message(message.chat.id, f"<pre>⏳ 𝙎𝙏𝘼𝙍𝙏𝙄𝙉𝙂 {filename}...</pre>", parse_mode='HTML')
    loading_stages = [
        f"<pre>⏳ 𝙎𝙏𝘼𝙍𝙏𝙄𝙉𝙂 {filename} ▒▒▒▒▒▒▒▒▒▒ 0%</pre>",
        f"<pre>⏳ 𝙎𝙏𝘼𝙍𝙏𝙄𝙉𝙂 {filename} █▒▒▒▒▒▒▒▒▒ 10%</pre>",
        f"<pre>⏳ 𝙎𝙏𝘼𝙍𝙏𝙄𝙉𝙂 {filename} ██▒▒▒▒▒▒▒▒ 20%</pre>",
        f"<pre>⏳ 𝙎𝙏𝘼𝙍𝙏𝙄𝙉𝙂 {filename} ███▒▒▒▒▒▒▒ 30%</pre>",
        f"<pre>⏳ 𝙎𝙏𝘼𝙍𝙏𝙄𝙉𝙂 {filename} ████▒▒▒▒▒▒ 40%</pre>",
        f"<pre>⏳ 𝙎𝙏𝘼𝙍𝙏𝙄𝙉𝙂 {filename} █████▒▒▒▒▒ 50%</pre>",
        f"<pre>⏳ 𝙎𝙏𝘼𝙍𝙏𝙄𝙉𝙂 {filename} ██████▒▒▒▒ 60%</pre>",
        f"<pre>⏳ 𝙎𝙏𝘼𝙍𝙏𝙄𝙉𝙂 {filename} ███████▒▒▒ 70%</pre>",
        f"<pre>⏳ 𝙎𝙏𝘼𝙍𝙏𝙄𝙉𝙂 {filename} ████████▒▒ 80%</pre>",
        f"<pre>⏳ 𝙎𝙏𝘼𝙍𝙏𝙄𝙉𝙂 {filename} █████████▒ 90%</pre>",
        f"<pre>⏳ 𝙎𝙏𝘼𝙍𝙏𝙄𝙉𝙂 {filename} ██████████ 100%</pre>",
    ]

    for stage in loading_stages:
        bot.edit_message_text(
            stage,
            chat_id=message.chat.id,
            message_id=loading_msg.message_id,
            parse_mode='HTML'
        )
        time.sleep(0.4)

    log_path = os.path.join(LOGS_DIR, f"{filename}.log")

    def run_script():
        try:
            bot.edit_message_text(
                f"<pre>▶️ {filename} 𝙎𝙏𝘼𝙍𝙏𝙀𝘿... ⚙️</pre>",
                chat_id=message.chat.id,
                message_id=loading_msg.message_id,
                parse_mode='HTML'
            )

            with open(log_path, 'w') as log_file:
                proc = subprocess.Popen(['python3', filepath], stdout=log_file, stderr=log_file)
                processes[filename] = {'process': proc, 'start_time': time.time()}
                proc.wait()
                exit_code = proc.returncode
                print(f"[DEBUG] {filename} exited with code {exit_code}")

                if exit_code == 0:
                    bot.edit_message_text(
                        f"<pre>✅ {filename} 𝙍𝘼𝙉 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇𝙇𝙔 ⚡</pre>",
                        chat_id=message.chat.id,
                        message_id=loading_msg.message_id,
                        parse_mode='HTML'
                    )
                elif exit_code == -15:
                    bot.edit_message_text(
                        f"<pre>⛔ {filename} 𝙒𝘼𝙎 𝙎𝙏𝙊𝙋𝙋𝙀𝘿 𝙈𝘼𝙉𝙐𝘼𝙇𝙇𝙔 ⚡</pre>",
                        chat_id=message.chat.id,
                        message_id=loading_msg.message_id,
                        parse_mode='HTML'
                    )
                else:
                    bot.edit_message_text(
                        f"<pre>❌ 𝙀𝙍𝙍𝙊𝙍 𝙄𝙉 {filename} ⚡\n📄 𝘾𝙃𝙀𝘾𝙆 𝙇𝙊𝙂: /log {filename}</pre>",
                        chat_id=message.chat.id,
                        message_id=loading_msg.message_id,
                        parse_mode='HTML'
                    )
        except Exception as e:
            bot.edit_message_text(
                f"<pre>❌ 𝙀𝙓𝘾𝙀𝙋𝙏𝙄𝙊𝙉 𝙒𝙃𝙄𝙇𝙀 𝙍𝙐𝙉𝙉𝙄𝙉𝙂 {filename} ⚡\n{str(e)}\n\n📄 /log {filename}</pre>",
                chat_id=message.chat.id,
                message_id=loading_msg.message_id,
                parse_mode='HTML'
            )
        finally:
            processes.pop(filename, None)

    threading.Thread(target=run_script).start()
        
@bot.message_handler(commands=['stopfile'])
def stop_file(message):
    parts = message.text.strip().split(' ', 1)
    if len(parts) < 2:
        return bot.reply_to(message, "⚠️ 𝙐𝙎𝙀 `/stopfile filename.py`", parse_mode='Markdown')

    filename = parts[1].strip()
    status = bot.reply_to(message, f"<pre>⛔ 𝙎𝙏𝙊𝙋𝙋𝙄𝙉𝙂 {filename}...</pre>", parse_mode='HTML')

    time.sleep(1)
    if filename in processes:
        processes[filename]['process'].terminate()
        del processes[filename]
        bot.edit_message_text(f"<pre>✅ {filename} 𝙎𝙏𝙊𝙋𝙋𝙀𝘿 ⚡</pre>", chat_id=message.chat.id, message_id=status.message_id, parse_mode='HTML')
    else:
        bot.edit_message_text(f"<pre>❌ {filename} 𝙉𝙊𝙏 𝙍𝙐𝙉𝙉𝙄𝙉𝙂 ⚡</pre>", chat_id=message.chat.id, message_id=status.message_id, parse_mode='HTML')

@bot.message_handler(commands=['stopall'])
def stop_all_scripts(message):
    status = bot.reply_to(message, "<pre>🛑 𝙏𝙀𝙍𝙈𝙄𝙉𝘼𝙏𝙄𝙉𝙂 𝘼𝙇𝙇 𝙎𝘾𝙍𝙄𝙋𝙏𝙎...</pre>", parse_mode='HTML')
    time.sleep(1)

    count = 0
    for filename in list(processes.keys()):
        try:
            processes[filename]['process'].terminate()
            del processes[filename]
            count += 1
        except:
            continue

    bot.edit_message_text(f"<pre>✅ {count} 𝙎𝘾𝙍𝙄𝙋𝙏𝙎 𝙎𝙏𝙊𝙋𝙋𝙀𝘿 ⚡</pre>", chat_id=message.chat.id, message_id=status.message_id, parse_mode='HTML')
                
@bot.callback_query_handler(func=lambda call: call.data == "uploaded_files")
def uploaded_files_callback(call):
    import html

    user_dir = os.path.join(UPLOAD_DIR, str(call.message.chat.id))

    if not os.path.exists(user_dir):
        return bot.answer_callback_query(call.id, "📭 𝙉𝙊 𝙁𝙄𝙇𝙀𝙎 𝙁𝙊𝙐𝙉𝘿⚡.")
    
    files = [f for f in os.listdir(user_dir) if os.path.isfile(os.path.join(user_dir, f))]
    if not files:
        return bot.edit_message_text(
            "📂 <b>𝙉𝙊 𝙐𝙋𝙇𝙊𝘼𝘿𝙀𝘿 𝙁𝙄𝙇𝙀𝙎 𝘼𝙑𝘼𝙄𝙇𝘼𝘽𝙇𝙀 ⚡</b>",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            parse_mode='HTML'
        )

    def escape_html(text):
        return html.escape(text)

    file_list = '\n'.join([f"📄 {escape_html(file)}" for file in files])

    animated_msg = (
        "📂 <b>𝙔𝙊𝙐𝙍 𝙐𝙋𝙇𝙊𝘼𝘿𝙀𝘿 𝙁𝙄𝙇𝙀𝙎⚡</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"<pre>{file_list}</pre>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🛠️ Use /startfile &lt;filename&gt; to run"
    )

    bot.edit_message_text(
        animated_msg,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        parse_mode='HTML'
    )
    
@bot.callback_query_handler(func=lambda call: call.data == "upload_file")
def ask_for_upload(call):
    bot.send_message(call.message.chat.id, "📥 𝙎𝙀𝙉𝘿 𝙔𝙊𝙐𝙍 .𝙥𝙮 𝙁𝙄𝙇𝙀𝙎 𝙏𝙊 𝙐𝙋𝙇𝙊𝘼𝘿 𝙄𝙏 ⚡.")                

@bot.message_handler(commands=['deletefile'])
def delete_file(message):
    filename = message.text.split(' ', 1)[-1].strip()
    user_dir = os.path.join(UPLOAD_DIR, str(message.chat.id))
    filepath = os.path.join(user_dir, filename)

    if os.path.exists(filepath):
        if filename in processes:
            processes[filename]['process'].terminate()
            del processes[filename]
        os.remove(filepath)
        bot.reply_to(message, f"<pre>🗑️ {filename} 𝘿𝙀𝙇𝙀𝙏𝙀𝘿 ⚡</pre>", parse_mode='HTML')
    else:
        bot.reply_to(message, f"<pre>❌ {filename} 𝙉𝙊𝙏 𝙁𝙊𝙐𝙉𝘿 ⚡</pre>", parse_mode='HTML')

@bot.message_handler(commands=['deleteall'])
def delete_all_files(message):
    user_dir = os.path.join(UPLOAD_DIR, str(message.chat.id))
    if os.path.exists(user_dir) and os.listdir(user_dir):
        for f in os.listdir(user_dir):
            path = os.path.join(user_dir, f)
            if os.path.isfile(path):
                os.remove(path)
        bot.reply_to(message, "<pre>🧹 𝘼𝙇𝙇 𝙁𝙄𝙇𝙀𝙎 𝘿𝙀𝙇𝙀𝙏𝙀𝘿 ⚡</pre>", parse_mode='HTML')
    else:
        bot.reply_to(message, "<pre>📭 𝙉𝙊 𝙁𝙄𝙇𝙀𝙎 𝙏𝙊 𝘿𝙀𝙇𝙀𝙏𝙀 ⚡</pre>", parse_mode='HTML')

@bot.message_handler(commands=['listfiles'])
def list_files(message):
    if processes:
        lines = []
        for name, proc in processes.items():
            runtime = int(time.time() - proc['start_time'])
            bar = "█" * min(runtime * 10 // EXECUTION_TIMEOUT, 10)
            bar += "░" * (10 - len(bar))
            lines.append(f"• {name} — [{bar}] {runtime}s")

        file_list = "\n".join(lines)
        reply_text = (
            "📂 <b>𝘼𝘾𝙏𝙄𝙑𝙀 𝙁𝙄𝙇𝙀𝙎⚡:</b>\n"
            f"<pre>{file_list}</pre>"
        )
        bot.reply_to(message, reply_text, parse_mode='HTML')
    else:
        bot.reply_to(message, "📭 𝙉𝙊 𝘼𝘾𝙏𝙄𝙑𝙀 𝙁𝙄𝙇𝙀𝙎 𝙍𝙐𝙉𝙉𝙄𝙉𝙂.⚡")
        
@bot.message_handler(commands=['renamefile'])
def rename_file(message):
    if not is_approved(message.from_user.id):
        return bot.reply_to(message, "❌ 𝙔𝙊𝙐 𝘼𝙍𝙀 𝙉𝙊𝙏 𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝘿⚡.")
    try:
        _, old, new = message.text.split()
        user_dir = os.path.join(UPLOAD_DIR, str(message.chat.id))
        old_path = os.path.join(user_dir, old)
        new_path = os.path.join(user_dir, new)
        if os.path.exists(old_path):
            os.rename(old_path, new_path)
            bot.reply_to(message, f"✅ 𝙍𝙀𝙉𝘼𝙈𝙀𝘿 `{old}` to `{new}`", parse_mode='Markdown')
        else:
            bot.reply_to(message, f"❌ 𝙁𝙄𝙇𝙀 `{old}` 𝙉𝙊𝙏 𝙁𝙊𝙐𝙉𝘿⚡.", parse_mode='Markdown')
    except:
        bot.reply_to(message, "𝙐𝙎𝘼𝙂𝙀⚡: /renamefile <old_filename> <new_filename>")        

@bot.message_handler(commands=['getlog'])
def get_log(message):
    if not is_approved(message.from_user.id):
        return bot.reply_to(message, "<pre>❌ 𝙔𝙊𝙐 𝘼𝙍𝙀 𝙉𝙊𝙏 𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝘿 ⚡</pre>", parse_mode='HTML')

    parts = message.text.strip().split(' ', 1)
    if len(parts) < 2 or not parts[1].strip():
        return bot.send_message(message.chat.id, "⚠️ 𝙐𝙎𝘼𝙂𝙀:\n<pre>/getlog filename.py</pre>", parse_mode='HTML')

    filename = re.sub(r'[^\w\.-]', '_', parts[1].strip())
    log_path = os.path.join(LOGS_DIR, f"{filename}.log")

    loading = bot.send_message(message.chat.id, f"<pre>📄 𝙁𝙄𝙉𝘿𝙄𝙉𝙂 𝙇𝙊𝙂 {filename}...</pre>", parse_mode='HTML')
    if not loading:
        return bot.send_message(message.chat.id, "❌ Could not send log request message.")

    anim = [
        f"<pre>🔍 𝘾𝙃𝙀𝘾𝙆𝙄𝙉𝙂 ▒▒▒▒▒▒▒▒▒▒ 0%</pre>",
        f"<pre>🔍 𝘾𝙃𝙀𝘾𝙆𝙄𝙉𝙂 █▒▒▒▒▒▒▒▒▒ 10%</pre>",
        f"<pre>🔍 𝘾𝙃𝙀𝘾𝙆𝙄𝙉𝙂 ██▒▒▒▒▒▒▒▒ 20%</pre>",
        f"<pre>🔍 𝘾𝙃𝙀𝘾𝙆𝙄𝙉𝙂 ███▒▒▒▒▒▒▒ 30%</pre>",
        f"<pre>🔍 𝘾𝙃𝙀𝘾𝙆𝙄𝙉𝙂 ████▒▒▒▒▒▒ 40%</pre>",
        f"<pre>🔍 𝘾𝙃𝙀𝘾𝙆𝙄𝙉𝙂 █████▒▒▒▒▒ 50%</pre>",
        f"<pre>🔍 𝘾𝙃𝙀𝘾𝙆𝙄𝙉𝙂 ██████▒▒▒▒ 60%</pre>",
        f"<pre>🔍 𝘾𝙃𝙀𝘾𝙆𝙄𝙉𝙂 ███████▒▒▒ 70%</pre>",
        f"<pre>🔍 𝘾𝙃𝙀𝘾𝙆𝙄𝙉𝙂 ████████▒▒ 80%</pre>",
        f"<pre>🔍 𝘾𝙃𝙀𝘾𝙆𝙄𝙉𝙂 █████████▒ 90%</pre>",
        f"<pre>🔍 𝘾𝙃𝙀𝘾𝙆𝙄𝙉𝙂 ██████████ 100%</pre>",
    ]

    for stage in anim:
        bot.edit_message_text(stage, chat_id=message.chat.id, message_id=loading.message_id, parse_mode='HTML')
        time.sleep(0.3)

    if not os.path.exists(log_path):
        return bot.edit_message_text(f"<pre>❌ 𝙇𝙊𝙂 𝙁𝙄𝙇𝙀 𝙉𝙊𝙏 𝙁𝙊𝙐𝙉𝘿 ⚡\nFilename: {filename}</pre>", chat_id=message.chat.id, message_id=loading.message_id, parse_mode='HTML')

    if os.path.getsize(log_path) == 0:
        return bot.edit_message_text(f"<pre>📭 𝙇𝙊𝙂 𝙄𝙎 𝙀𝙈𝙋𝙏𝙔 ⚡\nFilename: {filename}</pre>", chat_id=message.chat.id, message_id=loading.message_id, parse_mode='HTML')

    with open(log_path, 'rb') as log_file:
        bot.send_document(message.chat.id, log_file, caption=f"<pre>📄 LOG FILE: {filename}</pre>", parse_mode='HTML')
        
@bot.message_handler(commands=['log'])
def log_command(message):
    if not is_approved(message.from_user.id):
        return bot.reply_to(
            message,
            "<pre>❌ 𝙔𝙊𝙐 𝘼𝙍𝙀 𝙉𝙊𝙏 𝘼𝙐𝙏𝙃𝙊𝙍𝙄𝙕𝙀𝘿 ⚡</pre>",
            parse_mode='HTML'
        )

    parts = message.text.strip().split(' ', 1)
    if len(parts) < 2 or not parts[1].strip():
        return bot.reply_to(
            message,
            "⚠️ 𝙐𝙎𝘼𝙂𝙀:\n<pre>/log filename.py</pre>",
            parse_mode='HTML'
        )

    filename = re.sub(r'[^\w\.-]', '_', parts[1].strip())
    log_path = os.path.join(LOGS_DIR, f"{filename}.log")

    try:
        loading = bot.send_message(
            message.chat.id,
            f"<pre>📜 𝙇𝙊𝘼𝘿𝙄𝙉𝙂 𝙇𝙊𝙂: {filename}</pre>",
            parse_mode='HTML'
        )
    except Exception as e:
        return bot.reply_to(
            message,
            f"<pre>❌ Failed to start loading message:\n{str(e)}</pre>",
            parse_mode='HTML'
        )

    if not loading:
        return bot.reply_to(message, "❌ Internal error: loading message was not sent.")

    animation_frames = [
        "📜 𝙍𝙀𝘼𝘿𝙄𝙉𝙂 •──────────⚡",
        "📜 𝙍𝙀𝘼𝘿𝙄𝙉𝙂 ━•─────────⚡",
        "📜 𝙍𝙀𝘼𝘿𝙄𝙉𝙂 ━━•────────⚡",
        "📜 𝙍𝙀𝘼𝘿𝙄𝙉𝙂 ━━━•───────⚡",
        "📜 𝙍𝙀𝘼𝘿𝙄𝙉𝙂 ━━━━━•─────⚡",
        "📜 𝙍𝙀𝘼𝘿𝙄𝙉𝙂 ━━━━━━•────⚡",
        "📜 𝙍𝙀𝘼𝘿𝙄𝙉𝙂 ━━━━━━━•───⚡",
        "📜 𝙍𝙀𝘼𝘿𝙄𝙉𝙂 ━━━━━━━━•──⚡",
        "📜 𝙍𝙀𝘼𝘿𝙄𝙉𝙂 ━━━━━━━━━•─⚡",
        "📜 𝙍𝙀𝘼𝘿𝙄𝙉𝙂 ━━━━━━━━━━•⚡"
    ]

    for frame in animation_frames:
        try:
            bot.edit_message_text(
                f"<pre>{frame}</pre>",
                chat_id=message.chat.id,
                message_id=loading.message_id,
                parse_mode='HTML'
            )
            time.sleep(0.2)
        except Exception:
            break  # In case the message was deleted or edited

    if not os.path.exists(log_path):
        return bot.edit_message_text(
            f"<pre>❌ 𝙇𝙊𝙂 𝙁𝙄𝙇𝙀 𝙉𝙊𝙏 𝙁𝙊𝙐𝙉𝘿 ⚡\nFilename: {filename}</pre>",
            chat_id=message.chat.id,
            message_id=loading.message_id,
            parse_mode='HTML'
        )

    if os.path.getsize(log_path) == 0:
        return bot.edit_message_text(
            f"<pre>📭 𝙇𝙊𝙂 𝙄𝙎 𝙀𝙈𝙋𝙏𝙔 ⚡\nFilename: {filename}</pre>",
            chat_id=message.chat.id,
            message_id=loading.message_id,
            parse_mode='HTML'
        )

    try:
        with open(log_path, 'r', encoding='utf-8', errors='replace') as log_file:
            content = log_file.read()
            if len(content) > 4000:
                content = content[-3900:]  # Keep within Telegram limits
    except Exception as e:
        return bot.edit_message_text(
            f"<pre>❌ ERROR READING LOG ⚠️\n{str(e)}</pre>",
            chat_id=message.chat.id,
            message_id=loading.message_id,
            parse_mode='HTML'
        )

    content = html.escape(content)

    final_text = (
        f"<pre>📄 LOG FILE: {filename}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{content}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━</pre>"
    )

    bot.edit_message_text(
        final_text,
        chat_id=message.chat.id,
        message_id=loading.message_id,
        parse_mode='HTML'
    )
   
@bot.message_handler(commands=['health'])
@admin_only
def health_check(message):
    uptime = int(time.time() - START_TIME)
    running = len(processes)

    try:
        mem = psutil.virtual_memory()
        mem_percent = f"{mem.percent}%"
    except (PermissionError, FileNotFoundError):
        mem_percent = "Unavailable"

    health_msg = (
        "*✅ 𝘽𝙊𝙏 𝙃𝙀𝘼𝙇𝙏𝙃 𝙎𝙏𝘼𝙏𝙐𝙎⚡*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "<pre>\n"
        f"⏱ 𝙐𝙋𝙏𝙄𝙈𝙀        : {uptime} sec\n"
        f"📂 𝙍𝙐𝙉𝙉𝙄𝙉𝙂 𝙁𝙄𝙇𝙀𝙎: {running}\n"
        f"📈 𝙈𝙀𝙈𝙊𝙍𝙔 𝙐𝙎𝘼𝙂𝙀 : {mem_percent}\n"
        f"📤 𝙐𝙋𝙇𝙊𝘼𝘿 𝘾𝙊𝙐𝙉𝙏 : {file_upload_count}\n"
        "</pre>"
        "━━━━━━━━━━━━━━━━━━━━━━"
    )

    bot.send_message(message.chat.id, health_msg, parse_mode='HTML')  
    
@bot.message_handler(commands=['install'])
def install_modules(message):
    if not (is_premium(message.from_user.id) or message.from_user.id in ADMINS):
        return bot.reply_to(message, "❌ 𝙔𝙊𝙐 𝘼𝙍𝙀 𝙉𝙊𝙏 𝘼𝙐𝙏𝙃𝙊𝙍𝙄𝙕𝙀𝘿 𝙏𝙊 𝙐𝙎𝙀 /install ⚡.")

    try:
        parts = message.text.strip().split(maxsplit=1)
        if len(parts) != 2:
            return bot.reply_to(message, "⚠️ 𝙐𝙎𝘼𝙂𝙀⚡: `/install filename.py`", parse_mode='Markdown')

        filename = parts[1].strip()
        user_dir = os.path.join(UPLOAD_DIR, str(message.chat.id))
        filepath = os.path.join(user_dir, filename)

        if not os.path.exists(filepath):
            return bot.reply_to(message, f"❌ 𝙁𝙄𝙇𝙀 `{filename}` 𝙉𝙊𝙏 𝙁𝙊𝙐𝙉𝘿 ⚡", parse_mode='Markdown')

        with open(filepath, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=filename)

        modules = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.update(alias.name.split('.')[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    modules.add(node.module.split('.')[0])

        if not modules:
            return bot.reply_to(message, "✅ 𝙉𝙊 𝙈𝙊𝘿𝙐𝙇𝙀𝙎 𝙁𝙊𝙐𝙉𝘿 ⚡")

        installed, already, errors = [], [], []

        for mod in sorted(modules):
            try:
                __import__(mod)
                already.append(mod)
            except ImportError:
                try:
                    result = subprocess.run(
                        [sys.executable, "-m", "pip", "install", mod],
                        capture_output=True,
                        text=True
                    )
                    if result.returncode == 0:
                        installed.append(mod)
                    else:
                        errors.append(mod)
                except Exception:
                    errors.append(mod)

        reply = "📦 *𝙈𝙊𝘿𝙐𝙇𝙀 𝙄𝙉𝙎𝙏𝘼𝙇𝙇 𝙎𝙏𝘼𝙏𝙐𝙎⚡*\n"
        reply += "━━━━━━━━━━━━━━━━━━━━━━\n<pre>\n"
        if installed:
            reply += f"✅ 𝙄𝙉𝙎𝙏𝘼𝙇𝙇𝙀𝘿     : {', '.join(installed)}\n"
        if already:
            reply += f"♻️ 𝘼𝙇𝙍𝙀𝘼𝘿𝙔 𝙏𝙃𝙀𝙍𝙀 : {', '.join(already)}\n"
        if errors:
            reply += f"❌ 𝙀𝙍𝙍𝙊𝙍𝙎        : {', '.join(errors)}\n"
        reply += "</pre>\n━━━━━━━━━━━━━━━━━━━━━━"

        bot.send_message(message.chat.id, reply, parse_mode='HTML')

    except Exception as e:
        bot.reply_to(message, f"❌ 𝙀𝙍𝙍𝙊𝙍 ⚡: `{str(e)}`", parse_mode='Markdown')
                    
@bot.message_handler(commands=['stats'])
def show_stats(message):
    uptime = int(time.time() - START_TIME)
    msg = (
        "⏱️ 𝘽𝙊𝙏 𝙎𝙏𝘼𝙏𝙎 🚀\n"
        "━━━━━━━━━━━━━━━\n"
        "<pre>\n"
        f"⏱ 𝙐𝙋𝙏𝙄𝙈𝙀⚡        : {uptime}s\n"
        f"📦 𝙁𝙄𝙇𝙀𝙎 𝙐𝙋𝙇𝙊𝘼𝘿𝙀𝘿⚡ : {file_upload_count}\n"
        "</pre>"
    )
    bot.send_message(message.chat.id, msg, parse_mode='HTML')

@bot.message_handler(commands=['approve'])
@admin_only
def approve_user(message):
    try:
        user_id = int(message.text.split()[1])
        status = bot.reply_to(message, "<pre>🔍 𝘾𝙃𝙀𝘾𝙆𝙄𝙉𝙂 𝙐𝙎𝙀𝙍 𝙄𝘿...</pre>", parse_mode='HTML')
        time.sleep(0.8)

        bot.edit_message_text("<pre>🔐 𝙂𝙍𝘼𝙉𝙏𝙄𝙉𝙂 𝘼𝘾𝘾𝙀𝙎𝙎...</pre>", chat_id=message.chat.id, message_id=status.message_id, parse_mode='HTML')
        time.sleep(0.8)

        if user_id not in approved_users:
            approved_users.append(user_id)
            save_approved_users()

            bot.edit_message_text(f"<pre>✅ 𝙐𝙎𝙀𝙍 {user_id} 𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝘿 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇𝙇𝙔!</pre>", chat_id=message.chat.id, message_id=status.message_id, parse_mode='HTML')

            try:
                bot.send_message(user_id,
                    "⚡ *𝘼𝘾𝘾𝙀𝙎𝙎 𝙂𝙍𝘼𝙉𝙏𝙀𝘿!*\n\n"
                    "𝙔𝙊𝙐 𝙃𝘼𝙑𝙀 𝘽𝙀𝙀𝙉 *𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝘿* 𝙏𝙊 𝙐𝙎𝙀 𝙏𝙃𝙀 𝘽𝙊𝙏.",
                    parse_mode='Markdown')
            except:
                pass
        else:
            bot.edit_message_text(f"<pre>⚠️ 𝙐𝙎𝙀𝙍 {user_id} 𝘼𝙇𝙍𝙀𝘼𝘿𝙔 𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝘿 ⚡</pre>", chat_id=message.chat.id, message_id=status.message_id, parse_mode='HTML')

    except:
        bot.reply_to(message, "⚠️ 𝙐𝙎𝘼𝙂𝙀⚡: /approve <user_id>")

@bot.message_handler(commands=['unapprove'])
@admin_only
def unapprove_user(message):
    try:
        user_id = int(message.text.split()[1])
        status = bot.reply_to(message, "<pre>🧹 𝙍𝙀𝙑𝙊𝙆𝙄𝙉𝙂 𝘼𝘾𝘾𝙀𝙎𝙎...</pre>", parse_mode='HTML')
        time.sleep(0.8)

        if user_id in approved_users:
            approved_users.remove(user_id)
            save_approved_users()

            bot.edit_message_text(f"<pre>❌ 𝙐𝙎𝙀𝙍 {user_id} 𝙐𝙉𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝘿 𝙎𝙐𝘾𝘾𝙀𝙎𝙎𝙁𝙐𝙇𝙇𝙔 ⚡</pre>", chat_id=message.chat.id, message_id=status.message_id, parse_mode='HTML')

            try:
                bot.send_message(user_id,
                    "⚠️ *𝘼𝘾𝘾𝙀𝙎𝙎 𝙍𝙀𝙑𝙊𝙆𝙀𝘿!*\n\n"
                    "𝙔𝙊𝙐 𝙃𝘼𝙑𝙀 𝘽𝙀𝙀𝙉 *𝙐𝙉𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝘿*.\n𝙔𝙊𝙐 𝘾𝘼𝙉 𝙉𝙊 𝙇𝙊𝙉𝙂𝙀𝙍 𝙐𝙎𝙀 𝘽𝙊𝙏 𝙁𝙀𝘼𝙏𝙐𝙍𝙀𝙎 ⚡",
                    parse_mode='Markdown')
            except:
                pass
        else:
            bot.edit_message_text(f"<pre>⚠️ 𝙐𝙎𝙀𝙍 {user_id} 𝙉𝙊𝙏 𝙁𝙊𝙐𝙉𝘿 𝙄𝙉 𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝘿 𝙇𝙄𝙎𝙏 ⚡</pre>", chat_id=message.chat.id, message_id=status.message_id, parse_mode='HTML')

    except:
        bot.reply_to(message, "⚠️ 𝙐𝙎𝘼𝙂𝙀⚡: /unapprove <user_id>")
        
@bot.message_handler(commands=['unapproveall'])
@admin_only
def unapprove_all(message):
    global approved_users
    old_users = approved_users.copy()
    approved_users = []
    save_approved_users()
    bot.reply_to(message, "❌ 𝘼𝙇𝙇 𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝘿 𝙐𝙎𝙀𝙍𝙎 𝙍𝙀𝙈𝙊𝙑𝙀𝘿 ⚡.")
    for uid in old_users:
        try:
            bot.send_message(uid, "🚫 𝙔𝙊𝙐𝙍 𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝘿 𝘼𝘾𝘾𝙀𝙎𝙎 𝙃𝘼𝙎 𝘽𝙀𝙀𝙉 𝙍𝙀𝙑𝙊𝙆𝙀𝘿 ⚡.")
        except: pass        

@bot.message_handler(commands=['user'])
@admin_only
def list_users(message):
    if not approved_users:
        return bot.reply_to(message, "📭 𝙉𝙊 𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝘿 𝙐𝙎𝙀𝙍𝙎 𝙔𝙀𝙏⚡.")
    
    result = "✅ *𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝘿 𝙐𝙎𝙀𝙍𝙎:*\n\n"
    for uid in approved_users:
        try:
            user = bot.get_chat(uid)
            result += f"- {user.first_name} ({uid})\n"
        except:
            result += f"- Unknown User ({uid})\n"
    bot.reply_to(message, result, parse_mode='Markdown')

@bot.message_handler(commands=['premiumusers'])
@admin_only
def list_premium_users(message):
    if not premium_users:
        return bot.reply_to(message, "📭 𝙉𝙊 𝙋𝙍𝙀𝙈𝙄𝙐𝙈 𝙐𝙎𝙀𝙍𝙎 𝙔𝙀𝙏⚡.")
    
    response = "⭐ *𝙋𝙍𝙀𝙈𝙄𝙐𝙈 𝙐𝙎𝙀𝙍𝙎:*\n\n"
    for uid in premium_users:
        try:
            user = bot.get_chat(uid)
            response += f"- {user.first_name} ({uid})\n"
        except:
            response += f"- Unknown User ({uid})\n"
    
    bot.reply_to(message, response, parse_mode='Markdown')

@bot.message_handler(commands=['premium'])
@admin_only
def make_premium(message):
    try:
        user_id = int(message.text.split()[1])
        if user_id not in premium_users:
            premium_users.append(user_id)
            save_premium_users()
            bot.reply_to(message, f"✅ 𝙐𝙎𝙀𝙍 {user_id} 𝙄𝙎 𝙉𝙊𝙒 𝙋𝙍𝙀𝙈𝙄𝙐𝙈.")

            # Notify the user
            try:
                bot.send_message(user_id,
                    "✨ *𝙋𝙍𝙀𝙈𝙄𝙐𝙈 𝘼𝘾𝙏𝙄𝙑𝘼𝙏𝙀𝘿!⚡*\n\n"
                    "⚡𝙉𝙊𝙒 𝙔𝙊𝙐 𝙃𝘼𝙑𝙀 *𝙋𝙍𝙀𝙈𝙄𝙐𝙈 𝘼𝘾𝘾𝙀𝙎𝙎*.\n"
                    "⚡𝙀𝙉𝙅𝙊𝙔 𝙐𝙉𝙇𝙄𝙈𝙄𝙏𝙀𝘿 𝙐𝙋𝙇𝙊𝘼𝘿 𝘼𝙉𝘿 𝙀𝙓𝘾𝙇𝙐𝙎𝙄𝙑𝙀 𝙁𝙀𝘼𝙏𝙐𝙍𝙀𝙎.",
                    parse_mode='Markdown')
            except:
                pass
        else:
            bot.reply_to(message, f"⚠️ 𝙐𝙎𝙀𝙍 {user_id} 𝙄𝙎 𝘼𝙇𝙍𝙀𝘼𝘿𝙔 𝙋𝙍𝙀𝙈𝙄𝙐𝙈.")
    except:
        bot.reply_to(message, "𝙐𝙎𝘼𝙂𝙀⚡: /premium <userid>")

@bot.message_handler(commands=['unpremium'])
@admin_only
def remove_premium(message):
    try:
        user_id = int(message.text.split()[1])
        if user_id in premium_users:
            premium_users.remove(user_id)
            save_premium_users()
            bot.reply_to(message, f"❌ 𝙍𝙀𝙈𝙊𝙑𝙀𝘿 𝙋𝙍𝙀𝙈𝙄𝙐𝙈 𝙁𝙍𝙊𝙈 𝙏𝙃𝙄𝙎 𝙐𝙎𝙀𝙍𝙎⚡ {user_id}")

            # Notify the user
            try:
                bot.send_message(user_id,
                    "🔒 *𝙋𝙍𝙀𝙈𝙄𝙐𝙈 𝙍𝙀𝙈𝙊𝙑𝙀𝘿!⚡*\n\n"
                    "𝙔𝙊𝙐𝙍 *𝙋𝙍𝙀𝙈𝙄𝙐𝙈 𝘼𝘾𝘾𝙀𝙎𝙎* 𝙃𝘼𝙎 𝘽𝙀𝙀𝙉 𝙍𝙀𝙑𝙊𝙆𝙀𝘿⚡.\n"
                    "𝙏𝙊 𝙐𝙋𝙂𝙍𝘼𝘿𝙀 𝘼𝙂𝘼𝙄𝙉, 𝘾𝙊𝙉𝙏𝘼𝘾𝙏 @SP1DEYYXPR1ME.",
                    parse_mode='Markdown')
            except:
                pass
        else:
            bot.reply_to(message, f"⚠️ 𝙐𝙎𝙀𝙍 {user_id} 𝙄𝙎 𝙉𝙊𝙏 𝙋𝙍𝙀𝙈𝙄𝙐𝙈.")
    except:
        bot.reply_to(message, "𝙐𝙎𝘼𝙂𝙀⚡: /unpremium <userid>")
        
@bot.message_handler(commands=['unpremiumall'])
@admin_only
def unpremium_all(message):
    global premium_users
    old_premiums = premium_users.copy()
    premium_users = []
    save_premium_users()
    bot.reply_to(message, "❌ 𝘼𝙇𝙇 𝙋𝙍𝙀𝙈𝙄𝙐𝙈 𝙐𝙎𝙀𝙍𝙎 𝙍𝙀𝙈𝙊𝙑𝙀𝘿 ⚡.")
    for uid in old_premiums:
        try:
            bot.send_message(uid, "🔒 𝙔𝙊𝙐𝙍 𝙋𝙍𝙀𝙈𝙄𝙐𝙈 𝘼𝘾𝘾𝙀𝙎𝙎 𝙃𝘼𝙎 𝘽𝙀𝙀𝙉 𝙍𝙀𝙈𝙊𝙑𝙀𝘿 ⚡.")
        except: pass        
        
@bot.message_handler(commands=['restart'])
@admin_only
def restart_bot(message):
    loading_msg = bot.reply_to(message, "♻️ 𝙍𝙀𝙎𝙏𝘼𝙍𝙏𝙄𝙉𝙂 ⚡...")

    stages = [
        "𝙍𝙚𝙨𝙩𝙖𝙧𝙩𝙞𝙣𝙜 ▒▒▒▒▒▒▒▒▒▒ 0%",
        "𝙍𝙚𝙨𝙩𝙖𝙧𝙩𝙞𝙣𝙜 █▒▒▒▒▒▒▒▒▒ 10%",
        "𝙍𝙚𝙨𝙩𝙖𝙧𝙩𝙞𝙣𝙜 ██▒▒▒▒▒▒▒▒ 20%",
        "𝙍𝙚𝙨𝙩𝙖𝙧𝙩𝙞𝙣𝙜 ███▒▒▒▒▒▒▒ 30%",
        "𝙍𝙚𝙨𝙩𝙖𝙧𝙩𝙞𝙣𝙜 ████▒▒▒▒▒▒ 40%",
        "𝙍𝙚𝙨𝙩𝙖𝙧𝙩𝙞𝙣𝙜 █████▒▒▒▒▒ 50%",
        "𝙍𝙚𝙨𝙩𝙖𝙧𝙩𝙞𝙣𝙜 ██████▒▒▒▒ 60%",
        "𝙍𝙚𝙨𝙩𝙖𝙧𝙩𝙞𝙣𝙜 ███████▒▒ 70%",
        "𝙍𝙚𝙨𝙩𝙖𝙧𝙩𝙞𝙣𝙜 ████████▒▒ 80%",
        "𝙍𝙚𝙨𝙩𝙖𝙧𝙩𝙞𝙣𝙜 █████████▒ 90%",
        "𝙍𝙚𝙨𝙩𝙖𝙧𝙩𝙞𝙣𝙜 ██████████ 100%\n\n♻️ 𝘽𝙊𝙏 𝙍𝙀𝙎𝙏𝘼𝙍𝙏 𝙎𝙄𝙈𝙐𝙇𝘼𝙏𝙀𝘿 ⚡"
    ]

    for stage in stages:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=loading_msg.message_id,
            text=stage
        )
        time.sleep(0.4)
    
@bot.message_handler(commands=['refresh'])
@admin_only
def refresh_bot(message):
    loading_msg = bot.reply_to(message, "🔄 𝙍𝙀𝙁𝙍𝙀𝙎𝙃𝙄𝙉𝙂 ⚡...")

    stages = [
        "𝙍𝙚𝙛𝙧𝙚𝙨𝙝𝙞𝙣𝙜 ▒▒▒▒▒▒▒▒▒▒ 0%",
        "𝙍𝙚𝙛𝙧𝙚𝙨𝙝𝙞𝙣𝙜 █▒▒▒▒▒▒▒▒▒ 10%",
        "𝙍𝙚𝙛𝙧𝙚𝙨𝙝𝙞𝙣𝙜 ██▒▒▒▒▒▒▒▒ 20%",
        "𝙍𝙚𝙛𝙧𝙚𝙨𝙝𝙞𝙣𝙜 ███▒▒▒▒▒▒▒ 30%",
        "𝙍𝙚𝙛𝙧𝙚𝙨𝙝𝙞𝙣𝙜 ████▒▒▒▒▒▒ 40%",
        "𝙍𝙚𝙛𝙧𝙚𝙨𝙝𝙞𝙣𝙜 █████▒▒▒▒▒ 50%",
        "𝙍𝙚𝙛𝙧𝙚𝙨𝙝𝙞𝙣𝙜 ██████▒▒▒▒ 60%",
        "𝙍𝙚𝙛𝙧𝙚𝙨𝙝𝙞𝙣𝙜 ███████▒▒▒ 70%",
        "𝙍𝙚𝙛𝙧𝙚𝙨𝙝𝙞𝙣𝙜 ████████▒▒ 80%",
        "𝙍𝙚𝙛𝙧𝙚𝙨𝙝𝙞𝙣𝙜 █████████▒ 90%",
        "𝙍𝙚𝙛𝙧𝙚𝙨𝙝𝙞𝙣𝙜 ██████████ 100%\n\n🔄 𝘽𝙊𝙏 𝙍𝙀𝙁𝙍𝙀𝙎𝙃 𝙎𝙄𝙈𝙐𝙇𝘼𝙏𝙀𝘿 ⚡"
    ]

    for stage in stages:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=loading_msg.message_id,
            text=stage
        )
        time.sleep(0.4)

@bot.message_handler(commands=['shutdown'])
@admin_only
def shutdown_bot(message):
    steps = [
        "⚠️ 𝐑𝐄𝐂𝐈𝐄𝐕𝐄𝐃 𝐒𝐇𝐔𝐓𝐃𝐎𝐖𝐍 𝐂𝐎𝐌𝐌𝐀𝐍𝐃...",
        "🔐 𝐒𝐀𝐕𝐈𝐍𝐆 𝐒𝐄𝐒𝐒𝐈𝐎𝐍 𝐃𝐀𝐓𝐀...",
        "📦 𝐂𝐋𝐎𝐒𝐈𝐍𝐆 𝐀𝐋𝐋 𝐓𝐀𝐒𝐊𝐒...",
        "📴 𝐄𝐗𝐈𝐓 𝐒𝐈𝐆𝐍𝐀𝐋 𝐒𝐄𝐍𝐓...",
        "🛑 𝐒𝐇𝐔𝐓𝐓𝐈𝐍𝐆 𝐃𝐎𝐖𝐍 𝐓𝐇𝐄 𝐁𝐎𝐓..."
    ]

    status = bot.reply_to(message, "⚙️ 𝐈𝐍𝐈𝐓𝐈𝐀𝐓𝐈𝐍𝐆 𝐁𝐎𝐓 𝐒𝐇𝐔𝐓𝐃𝐎𝐖𝐍...")

    for step in steps:
        bot.edit_message_text(
            f"<pre>{step}</pre>",
            chat_id=message.chat.id,
            message_id=status.message_id,
            parse_mode='HTML'
        )
        time.sleep(1)

    bot.edit_message_text(
        "<pre>💤 𝐁𝐎𝐓 𝐇𝐀𝐒 𝐁𝐄𝐄𝐍 𝐒𝐇𝐔𝐓 𝐃𝐎𝐖𝐍 𝐒𝐀𝐅𝐄𝐋𝐘.</pre>",
        chat_id=message.chat.id,
        message_id=status.message_id,
        parse_mode='HTML'
    )

    time.sleep(1)
    os._exit(0)

@bot.message_handler(commands=['broadcast'])
@admin_only
def broadcast(message):
    msg = message.text.replace('/broadcast', '').strip()
    if not msg:
        return bot.reply_to(message, "𝙐𝙎𝘼𝙂𝙀⚡: /broadcast <your message>")
    success = 0
    for uid in approved_users:
        try:
            bot.send_message(uid, f"📢 *𝘽𝙍𝙊𝘼𝘿𝘾𝘼𝙎𝙏⚡:*\n{msg}", parse_mode='Markdown')
            success += 1
        except:
            pass
    bot.reply_to(message, f"✅ 𝘽𝙍𝙊𝘼𝘿𝘾𝘼𝙎𝙏 𝙎𝙀𝙉𝙏 𝙏𝙊 {success} 𝙐𝙎𝙀𝙍𝙎.")

@bot.message_handler(commands=['myfiles'])
def handle_uploaded_files(message):
    import html

    user_dir = os.path.join(UPLOAD_DIR, str(message.chat.id))

    if not os.path.exists(user_dir):
        return bot.send_message(message.chat.id, "📂 <b>𝙉𝙊 𝙁𝙄𝙇𝙀𝙎 𝙁𝙊𝙐𝙉𝘿 ⚡</b>", parse_mode='HTML')

    files = [f for f in os.listdir(user_dir) if os.path.isfile(os.path.join(user_dir, f))]
    if not files:
        return bot.send_message(message.chat.id, "📂 <b>𝙉𝙊 𝙐𝙋𝙇𝙊𝘼𝘿𝙀𝘿 𝙁𝙄𝙇𝙀𝙎 ⚡</b>", parse_mode='HTML')

    def escape_html(text):
        return html.escape(text)

    file_list = '\n'.join([f"📄 {escape_html(file)}" for file in files])

    animated_msg = (
        "📁 <b>𝙔𝙊𝙐𝙍 𝙐𝙋𝙇𝙊𝘼𝘿𝙀𝘿 𝙁𝙄𝙇𝙀𝙎 ⚡</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n<pre>\n"
        f"{file_list}\n"
        "</pre>\n━━━━━━━━━━━━━━━━━━━━━━\n"
        "▶️ 𝙐𝙨𝙚 /startfile &lt;filename&gt; 𝙏𝙤 𝙍𝙪𝙣"
    )

    bot.send_message(message.chat.id, animated_msg, parse_mode='HTML')
    
@bot.message_handler(commands=['uptime'])
def uptime_command(message):
    uptime = int(time.time() - START_TIME)
    bot.send_message(message.chat.id, f"⏱️ 𝘽𝙊𝙏 𝙃𝘼𝙎 𝘽𝙀𝙀𝙉 𝙍𝙐𝙉𝙉𝙄𝙉𝙂 𝙁𝙊𝙍 {uptime} 𝙎𝙀𝘾𝙊𝙉𝘿𝙎⚡.")

@bot.message_handler(commands=['feedback'])
def handle_feedback(message):
    text = message.text.split(maxsplit=1)
    if len(text) < 2:
        return bot.reply_to(message, "⚠️ 𝙐𝙎𝘼𝙂𝙀: /feedback your message")

    status = bot.reply_to(message, "<pre>📝 𝙎𝙐𝘽𝙈𝙄𝙏𝙏𝙄𝙉𝙂 𝙁𝙀𝙀𝘿𝘽𝘼𝘾𝙆...</pre>", parse_mode='HTML')
    time.sleep(1)

    bot.edit_message_text("<pre>✅ 𝙁𝙀𝙀𝘿𝘽𝘼𝘾𝙆 𝙎𝙐𝘽𝙈𝙄𝙏𝙏𝙀𝘿 ⚡</pre>",
                          chat_id=message.chat.id,
                          message_id=status.message_id,
                          parse_mode='HTML')

    full_name = escape_markdown(message.from_user.first_name or "No Name")
    username = escape_markdown(f"@{message.from_user.username}") if message.from_user.username else "No Username"
    user_id = message.from_user.id
    feedback = escape_markdown(text[1])

    feedback_msg = (
        f"📩 *𝐅𝐄𝐄𝐃𝐁𝐀𝐂𝐊 𝐑𝐄𝐂𝐄𝐈𝐕𝐄𝐃\\!*\n\n"
        f"*Name:* `{full_name}`\n"
        f"*Username:* `{username}`\n"
        f"*User ID:* `{user_id}`\n\n"
        f"*Message:* \n{feedback}"
    )

    bot.send_message(OWNER_ID, feedback_msg, parse_mode='MarkdownV2')
    
@bot.message_handler(commands=['promote'])
@admin_only
def promote_admin(message):
    try:
        user_id = int(message.text.split()[1])
        if user_id not in ADMINS:
            ADMINS.append(user_id)
            save_admins()
            bot.reply_to(message, f"✅ 𝙋𝙍𝙊𝙈𝙊𝙏𝙀𝘿 {user_id} 𝙏𝙊 𝘼𝘿𝙈𝙄𝙉⚡.")

            # Notify the user
            try:
                bot.send_message(user_id,
                    "👑 *𝙔𝙊𝙐'𝙑𝙀 𝘽𝙀𝙀𝙉 𝙋𝙍𝙊𝙈𝙊𝙏𝙀𝘿!*\n\n"
                    "𝙉𝙊𝙒 𝙔𝙊𝙐 𝙃𝘼𝙑𝙀 *𝘼𝘿𝙈𝙄𝙉 𝘼𝘾𝘾𝙀𝙎𝙎*.\n"
                    "𝙐𝙎𝙀 /menu 𝙏𝙊 𝙀𝙓𝙋𝙇𝙊𝙍𝙀 𝙔𝙊𝙐𝙍 𝙉𝙀𝙒 𝙋𝙊𝙒𝙀𝙍𝙎!",
                    parse_mode='Markdown')
            except:
                pass
        else:
            bot.reply_to(message, f"⚠️ 𝙐𝙎𝙀𝙍 {user_id} 𝙄𝙎 𝘼𝙇𝙍𝙀𝘼𝘿𝙔 𝘼𝙉 𝘼𝘿𝙈𝙄𝙉⚡.")
    except:
        bot.reply_to(message, "𝙐𝙎𝘼𝙂𝙀⚡: /promote <user_id>")

@bot.message_handler(commands=['demote'])
@admin_only
def demote_admin(message):
    try:
        user_id = int(message.text.split()[1])
        if user_id == message.from_user.id:
            return bot.reply_to(message, "⚠️ 𝙔𝙊𝙐 𝘾𝘼𝙉𝙉𝙊𝙏 𝘿𝙀𝙈𝙊𝙏𝙀 𝙔𝙊𝙐𝙍𝙎𝙀𝙇𝙁⚡.")
        if user_id in ADMINS:
            ADMINS.remove(user_id)
            save_admins()
            bot.reply_to(message, f"❌ 𝘿𝙀𝙈𝙊𝙏𝙀𝘿 {user_id} 𝙁𝙍𝙊𝙈 𝘼𝘿𝙈𝙄𝙉⚡.")

            # Notify the user
            try:
                bot.send_message(user_id,
                    "⚠️ *𝘼𝘿𝙈𝙄𝙉 𝙍𝙄𝙂𝙃𝙏𝙎 𝙍𝙀𝙑𝙊𝙆𝙀𝘿!*\n\n"
                    "𝙔𝙊𝙐 𝘼𝙍𝙀 𝙉𝙊 𝙇𝙊𝙉𝙂𝙀𝙍 𝘼𝙉 𝘼𝘿𝙈𝙄𝙉.\n"
                    "𝙄𝙁 𝙔𝙊𝙐 𝘽𝙀𝙇𝙄𝙑𝙀 𝙏𝙃𝙄𝙎 𝙒𝘼𝙎 𝘼𝙉 𝙀𝙍𝙍𝙊𝙍 𝘾𝙊𝙉𝙏𝘼𝘾𝙏 𝙏𝙊 𝘼𝘿𝙈𝙄𝙉:-@SP1DEYYXPR1ME.",
                    parse_mode='Markdown')
            except:
                pass
        else:
            bot.reply_to(message, "⚠️ 𝙐𝙎𝙀𝙍 𝙄𝙎 𝙉𝙊𝙏 𝘼𝙉 𝘼𝘿𝙈𝙄𝙉⚡.")
    except:
        bot.reply_to(message, "𝙐𝙎𝘼𝙂𝙀⚡: /demote <user_id>")
             
@bot.message_handler(commands=['demoteall'])
@admin_only
def demote_all(message):
    global ADMINS
    user_id = message.from_user.id
    old_admins = ADMINS.copy()
    ADMINS = [user_id]
    save_admins()
    bot.reply_to(message, "❌ 𝘼𝙇𝙇 𝘼𝘿𝙈𝙄𝙉𝙎 𝘿𝙀𝙈𝙊𝙏𝙀𝘿, 𝙊𝙉𝙇𝙔 𝙔𝙊𝙐 𝙍𝙀𝙈𝘼𝙄𝙉 ⚡.")
    for uid in old_admins:
        if uid != user_id:
            try:
                bot.send_message(uid, "⚠️ 𝙔𝙊𝙐𝙍 𝘼𝘿𝙈𝙄𝙉 𝘼𝘾𝘾𝙀𝙎𝙎 𝙃𝘼𝙎 𝘽𝙀𝙀𝙉 𝙍𝙀𝙈𝙊𝙑𝙀𝘿 ⚡.")
            except: pass

@bot.message_handler(commands=['admins'])
@admin_only
def list_admins(message):
    result = "👑 *𝘾𝙐𝙍𝙍𝙀𝙉𝙏 𝘼𝘿𝙈𝙄𝙉𝙎⚡:*\n\n"
    for uid in ADMINS:
        try:
            user = bot.get_chat(uid)
            result += f"- {user.first_name} ({uid})\n"
        except:
            result += f"- Unknown ({uid})\n"
    bot.send_message(message.chat.id, result, parse_mode='Markdown')

@bot.message_handler(commands=['ask'])
def ask_admin(message):
    question = message.text.replace("/ask", "").strip()
    if not question:
        return bot.reply_to(message, "Usage: /ask <your question>")
    for admin_id in ADMINS:
        text = (
            f"❓ New Question from {message.from_user.first_name}\n"
            f"👤 @{message.from_user.username or 'None'}\n"
            f"🆔 {message.from_user.id}\n"
            f"💬 Question: {question}"
        )
        bot.send_message(admin_id, text, parse_mode="Markdown")
    bot.reply_to(message, "✅ Your question has been sent to the admin.")
    
@bot.callback_query_handler(func=lambda call: call.data == "view_menu")
def view_menu(call):
    if not is_approved(call.from_user.id):
        return bot.answer_callback_query(call.id, "❌ 𝙔𝙊𝙐 𝘼𝙍𝙀 𝙉𝙊𝙏 𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝘿.")

    # Build a fake message with correct from_user
    from telebot.types import Message
    fake_message = call.message
    fake_message.from_user = call.from_user

    # Now pass to menu_command
    menu_command(fake_message)

@bot.message_handler(commands=['check'])
@admin_only
def check_commands(message):
    class DummyUser:
        id = message.from_user.id
        first_name = "ADMINTEMP"
        username = "admin"

    class DummyMessage:
        def __init__(self, text):
            self.chat = type('obj', (object,), {'id': DummyUser.id})
            self.from_user = DummyUser()
            self.text = text
            self.message_id = 9999  # Fake message_id

    commands = {
        '/approve': approve_user,
        '/unapprove': unapprove_user,
        '/promote': promote_admin,
        '/demote': demote_admin,
        '/premium': make_premium,
        '/unpremium': remove_premium,
        '/broadcast': broadcast,
        '/restart': restart_bot,
        '/refresh': refresh_bot,
        '/stats': show_stats,
        '/uptime': uptime_command,
        '/renamefile': rename_file,
        '/listfiles': list_files,
        '/myfiles': handle_uploaded_files,
        '/feedback': handle_feedback,
        '/ask': ask_admin,
        '/user': list_users,
        '/premiumusers': list_premium_users,
        '/admins': list_admins,
       # '/startfile': start_file,
       # '/stopfile': stop_file,
       # '/deletefile': delete_file,
        '/getlog': get_log,
        '/menu': menu_command,
        # New additions
        '/demoteall': demote_all,
        '/unpremiumall': unpremium_all,
        '/unapproveall': unapprove_all,
        #'/deleteall': delete_all_files,
        #'/stopall': stop_all_files,
        '/log': log_command,
        '/disk': disk_usage,
        '/health': health_check,
        '/install': install_modules,
        '/schedule': schedule_script,
        '/myschedules': list_scheduled_scripts,
        '/unschedule': unschedule_script,
    }

    test_inputs = {
        '/approve': '/approve 12345678',
        '/unapprove': '/unapprove 12345678',
        '/promote': '/promote 12345678',
        '/demote': '/demote 12345678',
        '/premium': '/premium 12345678',
        '/unpremium': '/unpremium 12345678',
        '/broadcast': '/broadcast TEST MESSAGE',
        '/restart': '/restart',
        '/refresh': '/refresh',
        '/stats': '/stats',
        '/uptime': '/uptime',
        '/renamefile': '/renamefile old.py new.py',
        '/listfiles': '/listfiles',
        '/myfiles': '/myfiles',
        '/feedback': '/feedback NICE BOT',
        '/ask': '/ask HOW TO USE PREMIUM?',
        '/user': '/user',
        '/premiumusers': '/premiumusers',
        '/admins': '/admins',
        '/startfile': '/startfile example.py',
        '/getlog': '/getlog example.py',
        '/menu': '/menu',
        # New additions
        '/demoteall': '/demoteall',
        '/unpremiumall': '/unpremiumall',
        '/unapproveall': '/unapproveall',
        '/log': '/log example.py',
        '/disk': '/disk',
        '/health': '/health',
        '/install': '/install test.py',
        '/schedule': '/schedule test.py 23:59',
        '/myschedules': '/myschedules',
        '/unschedule': '/unschedule test.py',
    }

    from unittest.mock import patch
    result_lines = []
    for cmd, handler in commands.items():
        try:
            dummy_msg = DummyMessage(test_inputs[cmd])
            with patch.object(bot, 'reply_to', lambda *a, **kw: type('msg', (), {'message_id': 123, 'chat': type('obj', (), {'id': 999})})()), \
                 patch.object(bot, 'edit_message_text', lambda *a, **kw: None), \
                 patch.object(bot, 'send_message', lambda *a, **kw: None), \
                 patch.object(bot, 'send_document', lambda *a, **kw: None), \
                 patch.object(bot, 'get_chat', lambda uid: type('User', (), {"first_name": f"User{uid}"})):
                handler(dummy_msg)
            result_lines.append(f"***{cmd.lower()} ✅ 𝙒𝙊𝙍𝙆𝙄𝙉𝙂 ⚡***")
        except Exception as e:
            reason = str(e).splitlines()[0].upper()
            result_lines.append(f"***{cmd.lower()} ❌ 𝙄𝙎𝙎𝙐𝙀 ⚡ - {reason}***")

    bot.send_message(
        message.chat.id,
        "*🔍 𝘾𝙊𝙈𝙈𝘼𝙉𝘿 𝙃𝙀𝘼𝙇𝙏𝙃 𝘾𝙃𝙀𝘾𝙆⚡*\n\n" + "\n".join(result_lines),
        parse_mode='Markdown'
    )
    
@bot.message_handler(commands=['reply'])
def funny_reply(message):
    if message.from_user.id != OWNER_ID:
        return bot.reply_to(message, "❌ 𝙊𝙉𝙇𝙔 𝘽𝙊𝙏 𝙊𝙒𝙉𝙀𝙍 𝘾𝘼𝙉 𝙍𝙀𝙋𝙇𝙔 ⚡")

    parts = message.text.strip().split(maxsplit=2)
    if len(parts) < 3:
        return bot.reply_to(
            message,
            "⚠️ *Usage:*\n"
            "`/reply <chat_id or @username> <message>`\n\n"
            "✅ *Examples:*\n"
            "`/reply 123456789 Hello there!`\n"
            "`/reply @exampleuser Hello, this is a reply!`",
            parse_mode="Markdown"
        )

    target = parts[1]
    text = parts[2]

    try:
        # Resolve target to chat_id
        if target.startswith('@'):
            user = bot.get_chat(target)  # Get chat by username
            chat_id = user.id
        elif target.isdigit():
            chat_id = int(target)  # Treat as numeric chat_id
        else:
            return bot.reply_to(message, "❌ Invalid target. Provide a valid @username or numeric chat_id.")

        # Send the styled funny reply
        funny_msg = f"💬 *Funny Reply:*\n{text}\n\n✨ *Powered by Owner*"
        bot.send_chat_action(chat_id, 'typing')
        time.sleep(1)
        bot.send_message(chat_id, funny_msg, parse_mode='Markdown')
        bot.reply_to(message, f"✅ 𝙈𝙀𝙎𝙎𝘼𝙂𝙀 𝙎𝙀𝙉𝙏 𝙏𝙊 `{chat_id}` ⚡", parse_mode="Markdown")

    except telebot.apihelper.ApiException as api_error:
        if "chat not found" in str(api_error):
            bot.reply_to(message, "❌ 𝙀𝙍𝙍𝙊𝙍: Chat not found. Ensure the user has started the bot and the username or chat_id is correct.")
        else:
            bot.reply_to(message, f"❌ 𝙀𝙍𝙍𝙊𝙍: {api_error}")

    except Exception as e:
        bot.reply_to(message, f"❌ 𝙀𝙍𝙍𝙊𝙍: {e}") 
 
@bot.message_handler(commands=['disk'])
@admin_only
def disk_usage(message):
    total, used, free = shutil.disk_usage("/")
    total_gb = total // (2**30)
    used_gb = used // (2**30)
    free_gb = free // (2**30)
    percent = int((used / total) * 100)
    
    reply = (
        f"💽 𝘿𝙄𝙎𝙆 𝙐𝙎𝘼𝙂𝙀⚡:\n"
        f"━━━━━━━━━━━━━━━\n"
        f"<pre>"
        f"📦 𝙏𝙊𝙏𝘼𝙇⚡: {total_gb} 𝙂𝘽\n"
        f"📊 𝙐𝙎𝙀𝘿: {used_gb} 𝙂𝘽 ({percent}%)\n"
        f"🧹 𝙁𝙍𝙀𝙀: {free_gb} 𝙂𝘽\n"
        f"</pre>"
    )
    bot.send_message(message.chat.id, reply, parse_mode="HTML")              
@bot.message_handler(func=lambda message: message.text.startswith('/') and not any(
    message.text.startswith(cmd) for cmd in [
        '/start', '/menu', '/startfile', '/stopfile', '/deletefile', '/getlog',
        '/listfiles', '/myfiles', '/stats', '/uptime', '/feedback', '/ask',
        '/approve', '/unapprove', '/user', '/premium', '/unpremium',
        '/premiumusers', '/broadcast', '/restart', '/shutdown', '/renamefile',
        '/promote', '/demote', '/admins', '/check',
        # ✅ Add new ones here:
        '/demoteall', '/unpremiumall', '/unapproveall', '/deleteall', '/stopall'
    ]
))
def unknown_command(message):
    if not is_approved(message.from_user.id):
        return
    bot.reply_to(message, "❌ 𝙐𝙉𝙆𝙉𝙊𝙒𝙉 𝘾𝙊𝙈𝙈𝘼𝙉𝘿 ⚡. 𝙐𝙎𝙀 /menu 𝙏𝙊 𝙑𝙄𝙀𝙒 𝘼𝙇𝙇 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎.")
        
@bot.message_handler(commands=['menu'])
def menu_command(message):
    user_id = getattr(message.from_user, 'id', None) or getattr(message, 'chat', {}).get('id')
    if not is_approved(user_id):
        return bot.send_message(message.chat.id, "❌ 𝙔𝙊𝙐 𝘼𝙍𝙀 𝙉𝙊𝙏 𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝘿 𝙏𝙊 𝙐𝙎𝙀 𝙏𝙃𝙄𝙎 𝘽𝙊𝙏⚡.")

    # Rest same...
    
    menu_text = (
    "📘 *𝘽𝙊𝙏 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎:*\n"
    "━━━━━━━━━━━━━━━━━━━━━━\n"
    "▶️ `/startfile <filename>` – 𝙍𝙐𝙉 𝘼 𝙋𝙔𝙏𝙃𝙊𝙉 𝙁𝙄𝙇𝙀⚡\n"
    "🛑 `/stopfile <filename>` – 𝙎𝙏𝙊𝙋 𝘼 𝙁𝙄𝙇𝙀⚡\n"
    "🗑️ `/deletefile <filename>` – 𝘿𝙀𝙇𝙀𝙏𝙀 𝘼 𝙁𝙄𝙇𝙀⚡\n"
    "📄 `/getlog <filename>` – 𝙂𝙀𝙏 𝙇𝙊𝙂 𝙊𝙐𝙏𝙋𝙐𝙏⚡\n"
    "📜 `/log <filename>` – 𝙎𝙃𝙊𝙒 𝙇𝙊𝙂 𝙄𝙉 𝙈𝙀𝙎𝙎𝘼𝙂𝙀⚡\n"
    "📂 `/listfiles` – 𝙎𝙃𝙊𝙒 𝘼𝘾𝙏𝙄𝙑𝙀 𝙁𝙄𝙇𝙀𝙎⚡\n"
    "🗃️ `/myfiles` – 𝙎𝙀𝙀 𝙔𝙊𝙐𝙍 𝙁𝙄𝙇𝙀𝙎⚡\n"
    "📝 `/renamefile old.py new.py` – 𝙍𝙀𝙉𝘼𝙈𝙀 𝙁𝙄𝙇𝙀⚡\n"
    "🛑 `/stopall` – 𝙎𝙏𝙊𝙋 𝘼𝙇𝙇 𝙍𝙐𝙉𝙉𝙄𝙉𝙂 𝙁𝙄𝙇𝙀𝙎⚡\n"
    "🗑️ `/deleteall` – 𝘿𝙀𝙇𝙀𝙏𝙀 𝘼𝙇𝙇 𝙁𝙄𝙇𝙀𝙎⚡\n"
    "⏳ `/uptime` – 𝘽𝙊𝙏 𝙐𝙋𝙏𝙄𝙈𝙀⚡\n"
    "⏱️ `/stats` – 𝙐𝙋𝙏𝙄𝙈𝙀 + 𝙁𝙄𝙇𝙀 𝘾𝙊𝙐𝙉𝙏⚡\n"
    "❓ `/ask <question>` – 𝘼𝙎𝙆 𝘼𝘿𝙈𝙄𝙉⚡\n"
    "💬 `/feedback <msg>` – 𝙎𝙀𝙉𝘿 𝙁𝙀𝙀𝘿𝘽𝘼𝘾𝙆⚡\n"
    "⏰ /schedule `<file>` `<HH:MM>` -  𝙎𝘾𝙃𝙀𝘿𝙐𝙇𝙀 𝙎𝘾𝙍𝙄𝙋𝙏\n"
    "📅 /myschedules -  𝙑𝙄𝙀𝙒 𝙎𝘾𝙃𝙀𝘿𝙐𝙇𝙀𝘿 𝙁𝙄𝙇𝙀𝙎\n"
    " ❌ /unschedule `<file>` - 𝘾𝘼𝙉𝘾𝙀𝙇 𝙎𝘾𝙃𝙀𝘿𝙐𝙇𝙀𝘿 𝙁𝙄𝙇𝙀\n"
    
    "\n"
    "👑 *𝘼𝘿𝙈𝙄𝙉 𝙊𝙉𝙇𝙔 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎:*\n"
    "━━━━━━━━━━━━━━━━━━━━━━\n"
    "✅ `/approve <id>` – 𝘼𝙋𝙋𝙍𝙊𝙑𝙀 𝙐𝙎𝙀𝙍⚡\n"
    "❌ `/unapprove <id>` – 𝙍𝙀𝙈𝙊𝙑𝙀 𝙐𝙎𝙀𝙍⚡\n"
    "📋 `/user` – 𝙇𝙄𝙎𝙏 𝘼𝙋𝙋𝙍𝙊𝙑𝙀𝘿 𝙐𝙎𝙀𝙍𝙎⚡\n"
    "⭐ `/premium <id>` – 𝙂𝙄𝙑𝙀 𝙋𝙍𝙀𝙈𝙄𝙐𝙈⚡\n"
    "🚫 `/unpremium <id>` – 𝙍𝙀𝙈𝙊𝙑𝙀 𝙋𝙍𝙀𝙈𝙄𝙐𝙈⚡\n"
    "📜 `/premiumusers` – 𝙎𝙃𝙊𝙒 𝙋𝙍𝙀𝙈𝙄𝙐𝙈 𝙐𝙎𝙀𝙍𝙎⚡\n"
    "📢 `/broadcast <msg>` – 𝘽𝙍𝙊𝘼𝘿𝘾𝘼𝙎𝙏⚡\n"
    "♻️ `/restart` – 𝙍𝙀𝙎𝙏𝘼𝙍𝙏 𝘽𝙊𝙏⚡\n"
    "🔄 `/refresh` – 𝙍𝙀𝙁𝙍𝙀𝙎𝙃 𝘽𝙊𝙏⚡\n"
    "🔒 `/shutdown` – 𝙎𝙃𝙐𝙏𝘿𝙊𝙒𝙉 𝘽𝙊𝙏⚡\n"
    "⚙️ `/check` – 𝘾𝙃𝙀𝘾𝙆 𝘾𝙊𝙈𝙈𝘼𝙉𝘿𝙎 𝙎𝙏𝘼𝙏𝙐𝙎⚡\n"
    "💾 `/disk` – 𝘾𝙃𝙀𝘾𝙆 𝘿𝙄𝙎𝙆 𝙐𝙎𝘼𝙂𝙀⚡\n"
    "⬆️ `/promote <id>` – 𝙈𝘼𝙆𝙀 𝘼𝘿𝙈𝙄𝙉⚡\n"
    "⬇️ `/demote <id>` – 𝙍𝙀𝙈𝙊𝙑𝙀 𝘼𝘿𝙈𝙄𝙉⚡\n"
    "👥 `/admins` – 𝙎𝙃𝙊𝙒 𝘼𝘿𝙈𝙄𝙉𝙎⚡\n"
    "🩺 `/health` – 𝘽𝙊𝙏 𝙃𝙀𝘼𝙇𝙏𝙃 𝘾𝙃𝙀𝘾𝙆⚡\n"
    "📦 `/install <file.py>` – 𝙄𝙉𝙎𝙏𝘼𝙇𝙇 𝙍𝙀𝙌𝙐𝙄𝙍𝙀𝘿 𝙈𝙊𝘿𝙐𝙇𝙀𝙎⚡\n"
    "⚠️ `/unapproveall` – 𝙍𝙀𝙈𝙊𝙑𝙀 𝘼𝙇𝙇 𝙐𝙎𝙀𝙍𝙎⚡\n"
    "🧹 `/clean` – 𝘾𝙇𝙀𝘼𝙉 𝙍𝘼𝙈 🚀\n"
    "⚠️ `/unpremiumall` – 𝙍𝙀𝙈𝙊𝙑𝙀 𝘼𝙇𝙇 𝙋𝙍𝙀𝙈𝙄𝙐𝙈𝙎⚡\n"
    "⚠️ `/demoteall` – 𝘿𝙀𝙈𝙊𝙏𝙀 𝘼𝙇𝙇 𝘼𝘿𝙈𝙄𝙉𝙎 (𝙀𝙓𝘾𝙀𝙋𝙏 𝙔𝙊𝙐)⚡\n"
)
    bot.send_message(message.chat.id, escape_markdown(menu_text), parse_mode='MarkdownV2')
    
print("⚔️𝐒𝐓𝐄𝐏𝐏𝐈𝐍𝐆 𝐈𝐍𝐓𝐎 𝐓𝐇𝐄 𝐄𝐑𝐀 𝐎𝐅 𝐒𝐏𝐈𝐃𝐄𝐘𝐘 ⚔️")

if __name__ == "__main__":
    while True:
        try:
            print("🤖 Bot is starting...")
            bot.polling(none_stop=True, interval=0)
        except Exception as e:
            print(f"⚠️ Bot crashed, restarting... Error: {e}")
            time.sleep(5)