from flask import Flask, request
from zalo_bot import Bot, Update
from zalo_bot.ext import Dispatcher, CommandHandler, MessageHandler, filters

app = Flask(__name__)

# Token mới của bạn đã được cập nhật
TOKEN = '3455528756803080573:kDvBpXsLcdixlNvEKflZtEcCxasbNDdagcBnfqMkkvMJNkrPVErzFyMmXVJEkmiF'
bot = Bot(token=TOKEN)

# Lệnh /de hoặc /start
async def get_exam(update: Update, context):
    msg = (
        "📚 **ĐỀ THI MỚI NHẤT TRÊN EXAMLY**\n\n"
        "🔗 Truy cập ngay: https://examly-online-project.vercel.app/\n"
        "Chúc bạn ôn luyện và làm bài tốt!"
    )
    await update.message.reply_text(msg)

# Lệnh /help
async def help_command(update: Update, context):
    await update.message.reply_text("🤖 Các lệnh hỗ trợ:\n- /de : Lấy liên kết đề thi mới nhất\n- /help : Xem hướng dẫn")

# Đăng ký xử lý lệnh
dispatcher = Dispatcher(bot, None, workers=0)
dispatcher.add_handler(CommandHandler('de', get_exam))
dispatcher.add_handler(CommandHandler('start', get_exam))
dispatcher.add_handler(CommandHandler('help', help_command))

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True)
        payload = data.get('result', data)
        update = Update.de_json(payload, bot)
        dispatcher.process_update(update)
        return 'ok', 200
    except Exception as e:
        print("Lỗi Webhook:", e)
        return 'error', 500

if __name__ == '__main__':
    # Chạy Webhook Server ở cổng 5000
    app.run(port=5000)