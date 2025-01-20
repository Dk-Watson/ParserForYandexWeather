import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Загрузка переменных из .env
load_dotenv()

# Токен бота из .env
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# Функция для парсинга погоды
def get_weather():
    # Настройки для Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Запуск в фоновом режиме (без открытия браузера)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Автоматическая установка и настройка chromedriver
    service = Service(ChromeDriverManager().install())

    # Инициализация драйвера
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # URL страницы с прогнозом погоды для Москвы
    url = 'https://yandex.ru/pogoda/moscow'

    # Открываем страницу
    driver.get(url)

    # Парсим данные
    try:
        # Находим блок с прогнозом на 7 дней
        forecast_block = driver.find_element(By.CLASS_NAME, 'forecast-briefly__days')

        # Находим все дни
        days = forecast_block.find_elements(By.CLASS_NAME, 'forecast-briefly__day')

        # Формируем сообщение с прогнозом
        weather_data = []
        for day in days[:7]:  # Берем только первые 7 элементов
            # Извлекаем дату
            date = day.find_element(By.CLASS_NAME, 'forecast-briefly__date').text.strip()

            # Извлекаем температуру днем
            day_temp = day.find_element(By.CLASS_NAME, 'forecast-briefly__temp_day').text.strip()
            day_temp = day_temp.replace("днём", "").strip()  # Убираем "днём"

            # Извлекаем температуру ночью
            night_temp = day.find_element(By.CLASS_NAME, 'forecast-briefly__temp_night').text.strip()
            night_temp = night_temp.replace("ночью", "").strip()  # Убираем "ночью"

            # Добавляем данные в сообщение
            weather_data.append(f"{date}: Днем {day_temp}, Ночью {night_temp}")

        # Закрываем браузер
        driver.quit()

        # Возвращаем прогноз
        return "\n".join(weather_data)
    except Exception as e:
        print(f'Ошибка при парсинге: {e}')
        driver.quit()
        return "Не удалось получить данные о погоде."


# Обработчик команды /start
async def start(update: Update, context: CallbackContext):
    # Приветственное сообщение
    await update.message.reply_text("Привет! Могу подсказать погоду в Москве.")

    # Создаем клавиатуру с кнопкой
    keyboard = [["Получить погоду"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    # Отправляем клавиатуру
    await update.message.reply_text("Нажмите кнопку ниже, чтобы получить прогноз погоды:", reply_markup=reply_markup)


# Обработчик текстовых сообщений
async def handle_message(update: Update, context: CallbackContext):
    text = update.message.text

    # Если пользователь нажал кнопку "Получить погоду"
    if text == "Получить погоду":
        # Получаем прогноз погоды
        weather = get_weather()

        # Отправляем прогноз пользователю
        await update.message.reply_text(weather)
    else:
        await update.message.reply_text("Используйте кнопку, чтобы получить прогноз погоды.")


# Основная функция
def main():
    # Создаем приложение бота
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаем бота
    application.run_polling()


if __name__ == "__main__":
    main()