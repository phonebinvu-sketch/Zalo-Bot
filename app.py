import os
import asyncio
from flask import Flask, request
from zalo_bot import Bot, Update

app = Flask(__name__)

# Lấy token và URL từ biến môi trường Render
TOKEN = os.environ.get("ZALO_BOT_TOKEN", "3455528756803080573:kDvBpXsLcdixlNvEKflZtEcCxasbNDdagcBnfqMkkvMJNkrPVErzFyMmXVJEkmiF")
bot = Bot(token=TOKEN) if TOKEN else None

# Tự động đăng ký Webhook với Zalo khi Server Render vừa bật lên
def auto_register_webhook():
    if bot:
        try:
            webhook_url = "https://zalo-bot-lqp4.onrender.com/webhook"
            print("⏳ Đang tự động đăng ký Webhook với Zalo...")
            res = asyncio.run(bot.set_webhook(url=webhook_url))
            if res:
                print("✅ Đã tự động kích hoạt Webhook Zalo thành công!")
            else:
                print("❌ Đăng ký Webhook thất bại.")
        except Exception as e:
            print("Lỗi tự động set webhook:", e)

# Gọi hàm tự động đăng ký
auto_register_webhook()

async def process_zalo_update(update_data):
    if not bot:
        return
        
    update = Update.de_json(update_data, bot)
    
    if update and update.message and update.message.text:
        text = update.message.text.strip()
        
        # Xử lý các lệnh /de, /start hoặc từ khóa "đề"
        if text in ["/de", "/start"] or "đề" in text.lower():
            msg = (
                "📚 **ĐỀ THI MỚI NHẤT TRÊN EXAMLY**\n\n"
                "🔗 Truy cập ngay: https://examly-online-project.vercel.app/\n\n"
                "Chúc bạn ôn luyện và làm bài tốt!"
            )
            await update.message.reply_text(msg)
            
        elif text == "/help":
            help_msg = (
                "🤖 **HƯỚNG DẪN SỬ DỤNG BOT**\n"
                "- Gõ `/de` hoặc `/start`: Lấy liên kết đề thi mới nhất\n"
                "- Gõ `/help`: Xem trợ giúp"
            )
            await update.message.reply_text(help_msg)

@app.route("/", methods=["GET"])
def home():
    return "Zalo Bot Server is running!", 200

@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    if request.method == "GET":
        return "ok", 200

    try:
        data = request.get_json(force=True, silent=True) or {}
        payload = data.get("result", data)

        if payload:
            asyncio.run(process_zalo_update(payload))

        return "ok", 200
    except Exception as e:
        print("Lỗi Webhook:", e)
        return "ok", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
