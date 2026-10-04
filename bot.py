import os
import logging
import html
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 🛡️ የደህንነት ሎግንግ ማዋቀር (Security Logging Setup)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(name)

# 🔑 የቦት ቶከን (የእርስዎ የተስተካከለ ሚስጥራዊ ቁልፍ)
TOKEN = "8985815201:AAFU84DvUnLvHUbgTSQTlzsQsHW55GQU1V4"

# የተጠቃሚዎች እና የነጋዴ ቻናሎች መዝገብ (Database Simulation)
REGISTERED_CHANNELS = set()
SUBSCRIBERS = set()  # አፑን ወይም ቦቱን የሚጠቀሙ ተጠቃሚዎች ዝርዝር ለግሎባል ማስታወቂያ

# 🚫 ጸያፍ እና ህገወጥ ቃላት ማጣሪያ (Content Moderation Firewall - Anti-Hacking & Discipline)
BANNED_KEYWORDS = ["ህገወጥ", "ጦር መሳሪያ", "ሐሰተኛ", "sex", "hack", "malware"]

def is_content_safe(text: str) -> bool:
    """ማንኛውም ፖስት ሲገባ ህገወጥ ወይም ጸያፍ ቃላት እንዳሉት የሚያጣራ የደህንነት ግድግዳ"""
    if not text:
        return True
    text_lower = text.lower()
    for word in BANNED_KEYWORDS:
        if word in text_lower:
            return False
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ቦቱ ሲጀመር የሚሰጠው ሰላምታ እና መመሪያ"""
    user = update.effective_user
    SUBSCRIBERS.add(user.id)
    
    welcome_text = (
        f"ሰላም <b>{html.escape(user.first_name)}</b>! 🌟\n\n"
        "እንኳን ወደ <b>'መሃይሟ ምሁር' (LBD.MBE.SBJ.SFA)</b> ሱፐር ፕላትፎርም በደህና መጡ።\n\n"
        "📡 የራስዎን ቻናል ለማያያዝ እና ማስታወቂያ ለመልቀቅ እባክዎ ቻናልዎን አድሚን (Admin) ያድርጉት።"
    )
    await update.message.reply_html(welcome_text)

async def register_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ነጋዴዎች ቻናላቸውን ከሲስተሙ ጋር የሚያያይዙበት ደህንነቱ የተጠበቀ ትዕዛዝ"""
    try:
        chat_id = update.effective_chat.id
        REGISTERED_CHANNELS.add(chat_id)
        await update.message.reply_text(
            "🎉 ቻናልዎ በተሳካ ሁኔታ ተያይዟል! ከ 3 ወር ነፃ የሙከራ ጊዜ በኋላ በውሉ መሰረት ይሰራል።"
        )
    except Exception as e:
        logger.error(f"Error in channel registration: {e}")
        await update.message.reply_text("⚠️ ስህተት አጋጥሟል! እባክዎ እንደገና ይሞክሩ።")

async def broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """🌟 የአድሚን/የፈጣሪ ልዩ ማዕከል (Founder's Hub): አዲስ ነገር ሲለቀቅ ለሁሉም ማስታወቂያ ማዳረስ"""
    ADMIN_ID = 123456789  # የእርስዎን ትክክለኛ የቴሌግራም አድሚን ID እዚህ ያስገቡ
    
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ ይቅርታ! ይህንን ትዕዛዝ መጠቀም የሚችሉት ዋናው አድሚን ብቻ ናቸው።")
        return

    message_text = " ".join(context.args)
    if not message_text:
        await update.message.reply_text("⚠️ እባክዎ የሚተላለፈውን መልዕክት አብረው ይጻፉ። ဥပမာ: /broadcast ሰላም ቤተሰቦች...")
        return

    success_count = 0
    for user_id in SUBSCRIBERS:
        try:
            await context.bot.send_message(chat_id=user_id, text=f"📢 <b>አዲስ መረጃ ከፈጣሪ ጠረጴዛ:</b>\n\n{message_text}", parse_mode="HTML")
            success_count += 1
        except Exception as e:
            logger.error(f"Failed to send broadcast to {user_id}: {e}")

    await update.message.reply_text(f"✅ ማስታወቂያው ለ {success_count} ተጠቃሚዎች ተዳርሷል!")

async def handle_channel_posts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ነጋዴዎች በቻናላቸው የሚለቁትን ፖስት (ጽሁፍ፣ ፎቶ፣ ቪዲዮ) የሚቀበል እና የሚመረምር ሞተር"""
    post = update.channel_post
    if not post:
        return

    caption = post.caption or post.text or ""
    if not is_content_safe(caption):
        logger.warning(f"Blocked inappropriate post in channel {post.chat.title}")
        return

    logger.info(f"Verified post processed from channel: {post.chat.title}")

def main():
    """ቦቱን የሚያስነሳው ዋናው ክፍል (Security Application Builder)"""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("register", register_channel))
    application.add_handler(CommandHandler("broadcast", broadcast_message))
    application.add_handler(MessageHandler(filters.ChatType.CHANNEL & (filters.TEXT | filters.PHOTO | filters.VIDEO), handle_channel_posts)) print("🚀 'መሃይሟ ምሁር' የደህንነት ቦት በሰላም ተነሳ... 24/7 እየሰራ ነው።")
    application.run_polling()

if name == "main":
    main() 
