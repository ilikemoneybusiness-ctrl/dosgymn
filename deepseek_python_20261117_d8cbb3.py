import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Включите логирование, чтобы видеть ошибки
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Токен вашего бота
BOT_TOKEN = "9089241964:AAGxiwMDTtK52FKHMa677vbipco5gNwCArM"

# Имя пользователя получателя (без @), которому нужно отправлять сводку
TARGET_USERNAME = "dirtyforces"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Чтобы сделать заказ, введите команду /order"
    )

async def order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    # 1. Сообщаем пользователю, что заказ принят
    await update.message.reply_text(
        f"✅ Заказ принят! Сводка отправлена оператору @{TARGET_USERNAME}."
    )

    # 2. Формируем текст сводки
    summary_text = (
        f"📦 **НОВЫЙ ЗАКАЗ**\n"
        f"👤 От: {user.full_name} (@{user.username})\n"
        f"🆔 ID: {user.id}\n"
        f"💬 Чат ID: {chat_id}\n"
        f"📝 Статус: Ожидает подтверждения\n"
        f"---\n"
        f"(Здесь должны быть позиции заказа, но пока это заглушка)"
    )

    try:
        # 3. Отправляем сообщение целевому пользователю
        await context.bot.send_message(
            chat_id=f"@{TARGET_USERNAME}",
            text=summary_text,
            parse_mode="Markdown"
        )
    except Exception as e:
        logging.error(f"Не удалось отправить сводку: {e}")
        await update.message.reply_text(
            "⚠️ Не удалось доставить сводку оператору. "
            "Возможно, оператор ещё не запускал бота."
        )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("order", order))

    print("Бот запущен...")
    app.run_polling()

if __name__ == '__main__':
    main()