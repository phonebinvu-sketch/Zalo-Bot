import os
import asyncio
from flask import Flask, request
from zalo_bot import Bot, Update

app = Flask(__name__)

# Lấy token từ Environment Variable trên Render
TOKEN = os.environ.get("ZALO_BOT_TOKEN")
bot = Bot(token=TOKEN) if TOKEN else None

# Hàm xử lý tin nhắn và phản hồi bất đồng bộ
async def process_zalo_update(update_data):
    if not bot:
        return
        
    update = Update.de_json(update_data, bot)
    
    # Kiểm tra xem có tin nhắn dạng văn bản không
    if update and update.message and update.message.text:
        text = update.message.text.strip()
        chat_id = update.message.chat.id
        
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

# Route trang chủ kiểm tra Server (Tránh 404)
@app.route("/", methods=["GET"])
def home():
    return "Zalo Bot Server is running!", 200

# Route tiếp nhận Webhook từ Zalo Bot
@app.route("/webhook", methods=["POST", "GET"])
def webhook():
    if request.method == "GET":
        return "ok", 200

    try:
        data = request.get_json(force=True, silent=True) or {}
        payload = data.get("result", data)

        if payload:
            # Chạy hàm async để xử lý và gửi tin nhắn
            asyncio.run(process_zalo_update(payload))

        return "ok", 200
    except Exception as e:
        print("Lỗi Webhook:", e)
        return "ok", 200  # Trả về 200 để Zalo không retry gửi liên tục khi lỗi

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
