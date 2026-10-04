import os
import logging
import html
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 🛡️ Security Logging Setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(name)

# 🔑 Bot Token
TOKEN = "8985815201:AAFU84DvUnLvHUbgTSQTlzsQsHW55GQU1V4"

# Database Simulation
REGISTERED_CHANNELS = set()
SUBSCRIBERS = set()

# 🚫 Content Moderation Firewall
BANNED_KEYWORDS = ["ህገወጥ", "ጦር መሳሪያ", "ሐሰተኛ", "sex", "hack", "malware"]

def is_content_safe(text: str) -> bool:
    """Firewall to check for banned keywords in channel posts"""
    if not text:
        return True
    text_lower = text.lower()
    for word in BANNED_KEYWORDS:
        if word in text_lower:
            return False
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handler"""
    user = update.effective_user
    SUBSCRIBERS.add(user.id)
    
    welcome_text = (
        f"ሰላም <b>{html.escape(user.first_name)}</b>! 🌟\n\n"
        "እንኳን ወደ <b>'መሃይሟ ምሁር' (LBD.MBE.SBJ.SFA)</b> ሱፐር ፕላትፎርም በደህና መጡ።\n\n"
        "📡 የራስዎን ቻናል ለማያያዝ እና ማስታወቂያ ለመልቀቅ እባክዎ ቻናልዎን አድሚን (Admin) ያድርጉት።"
    )
    await update.message.reply_html(welcome_text)

async def register_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Register channel command handler"""
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
    """Broadcast message to all subscribers (Admin only)"""
    ADMIN_ID = 123456789  # Replace with your actual Telegram Admin ID
    
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
    """Handle incoming channel posts with moderation"""
    post = update.channel_post
    if not post:
        return

    caption = post.caption or post.text or ""
    if not is_content_safe(caption):
        logger.warning(f"Blocked inappropriate post in channel {post.chat.title}")
        return

    logger.info(f"Verified post processed from channel: {post.chat.title}")

def main():
    """Main application runner"""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("register", register_channel))
    application.add_handler(CommandHandler("broadcast", broadcast_message))
    application.add_handler(MessageHandler(filters.ChatType.CHANNEL & (filters.TEXT | filters.PHOTO | filters.VIDEO), handle_channel_posts))
    
    print("Bot is running...")
    application.run_polling()

if name == "main":
    main() 
