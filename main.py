from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import tkinter as tk
from tkinter import ttk

# Функция для парсинга
def get_weather():
    # Настройки для Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Путь к Гугл Хром
    chrome_options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"

    # Установка chromedriver
    service = Service(ChromeDriverManager().install())

    # Инициализацтя драйвера
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # URL страницы
    url = 'https://yandex.ru/pogoda/moscow'

    # Открываем страницу
    driver.get(url)

    # Парсер
    try:
        # Находим блок с прогнозом
        forecast_block = driver.find_element(By.CLASS_NAME, 'forecast-briefly__days')

        days = forecast_block.find_elements(By.CLASS_NAME, 'forecast-briefly__day')

        # Очищаем предыдущие данные в таблице
        for row in tree.get_children():
            tree.delete(row)

        # Заполнение таблицы
        for day in days[:7]:  #
            # Извлекаем дату
            date = day.find_element(By.CLASS_NAME, 'forecast-briefly__date').text.strip()

            # Получает t днем
            day_temp = day.find_element(By.CLASS_NAME, 'forecast-briefly__temp_day').text.strip()
            day_temp = day_temp.replace("днём", "").strip()  # Убираем "днём"

            # Получает t ночью
            night_temp = day.find_element(By.CLASS_NAME, 'forecast-briefly__temp_night').text.strip()
            night_temp = night_temp.replace("ночью", "").strip()  # Убираем "ночью"

            # Добавляем данные в таблицу
            tree.insert("", "end", values=(date, day_temp, night_temp))
    except Exception as e:
        print(f'Ошибка при парсинге: {e}')
    finally:
        # Закрытие браузера
        driver.quit()

# Графическое окно
root = tk.Tk()
root.title("Прогноз погоды в Москве")
root.geometry("600x300")

# Таблица
columns = ("Дата", "Днем", "Ночью")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("Дата", text="Дата")
tree.heading("Днем", text="Днем")
tree.heading("Ночью", text="Ночью")
tree.pack(fill="both", expand=True)

# Кнопка обновления данных
update_button = tk.Button(root, text="Обновить", command=get_weather)
update_button.pack(pady=10)

# Запуск основного цикла
root.mainloop()