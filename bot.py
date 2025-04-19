# bot.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import requests

BOT_TOKEN = 'YOUR_BOT_TOKEN'
WHITELIST = [123456789, 987654321]

def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("Email Tools", callback_data='email')],
        [InlineKeyboardButton("Username Lookup", callback_data='username')],
        [InlineKeyboardButton("Phone Number", callback_data='phone')],
        [InlineKeyboardButton("IP Address", callback_data='ip')],
        [InlineKeyboardButton("Domain Info", callback_data='domain')],
        [InlineKeyboardButton("Social Media", callback_data='social')],
        [InlineKeyboardButton("Image/Metadata", callback_data='image')],
        [InlineKeyboardButton("Dark Web", callback_data='darkweb')],
        [InlineKeyboardButton("Leaks & Breaches", callback_data='leak')],
        [InlineKeyboardButton("Geolocation", callback_data='geo')],
        [InlineKeyboardButton("Pentest Tools", callback_data='pentest')],
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in WHITELIST:
        await update.message.reply_text("Access denied. You are not whitelisted.")
        return
    await update.message.reply_text("Welcome to OSINT Bot. Choose a category:", reply_markup=get_main_menu())

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    response = {
        'email': "Email OSINT Tools:\\n- haveibeenpwned.com\\n- emailrep.io\\n- hunter.io",
        'username': "Username Lookup:\\n- namechk.com\\n- whatsmyname.app\\n- sherlock",
        'phone': "Phone Trackers:\\n- numverify.com\\n- truecaller.com\\n- phoneinfoga",
        'ip': "IP OSINT:\\n- ipinfo.io\\n- shodan.io\\n- abuseipdb.com",
        'domain': "Domain Tools:\\n- whois\\n- crt.sh\\n- dnsdumpster.com",
        'social': "Social Media OSINT:\\n- Telegram Lookup\\n- Facebook Graph\\n- Twitter Search",
        'image': "Image Metadata:\\n- exif viewer\\n- fotoforensics.com\\n- reverse image search",
        'darkweb': "Dark Web:\\n- ahmia.fi\\n- onion.live\\n- hidden wiki",
        'leak': "Data Breach Tools:\\n- leakcheck.io\\n- snusbase\\n- weleakinfo (mirror)",
        'geo': "Geolocation Tools:\\n- exif GPS\\n- cell tower lookup\\n- google timeline",
        'pentest': "Pentest Tools:\\n- nmap\\n- recon-ng\\n- harvester\\n- dork generator"
    }.get(data, "Unknown category")

    await query.message.reply_text(response)

async def check_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in WHITELIST:
        await update.message.reply_text("Access denied.")
        return
    
    if len(context.args) == 0:
        await update.message.reply_text("Kirim: /email someone@example.com")
        return

    email = context.args[0]
    url = f"https://emailrep.io/{email}"
    headers = {'Key': 'API_KEY_EMAILREP'}

    try:
        res = requests.get(url, headers=headers).json()
        result = f"""
Email: {res.get('email', 'n/a')}
Reputation: {res.get('reputation', 'n/a')}
Suspicious: {res.get('suspicious', 'n/a')}
Blacklisted: {res.get('blacklisted', 'n/a')}
Sources: {', '.join(res.get('sources', []))}
        """
    except Exception as e:
        result = f"Gagal cek: {e}"

    await update.message.reply_text(result)

def log_history(user, query_type, query_input):
    with open("history.log", "a") as file:
        file.write(f"{user} | {query_type} | {query_input}\n")

async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in WHITELIST:
        await update.message.reply_text("Access denied.")
        return
    try:
        with open("history.log", "r") as f:
            lines = f.readlines()[-10:]  # tampilkan 10 terakhir
            await update.message.reply_text("Riwayat:\n" + "".join(lines))
    except:
        await update.message.reply_text("Belum ada riwayat.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(CommandHandler("email", check_email))
    app.add_handler(CommandHandler("history", history))
    print("Bot is running...")
    app.run_polling()
