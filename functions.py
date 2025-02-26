import pyttsx3  # Синтез речи

import webbrowser  # Открытие вкладок браузера
import datetime  # Работа со временем
import subprocess  # Запуск новых процессов
from pygame import mixer  # Воспроизведение записей
import traceback  # Формирование информации об исключениях
import requests  # Запросы на сайты
import keyboard  # Нажатие клавиш с помощью функций
import random  # Генератор случайных чисел
import json  # Работа с данными в формате JSON

engine = pyttsx3.init()
mixer.init()

appid = "b8674996d882d71cf243358cf5634257"

weather_type = json.loads(open('weather_type.json', encoding="UTF-8").read())
commands = json.loads(open('commands.json', encoding="UTF-8").read())
numbers = json.loads(open('numbers.json', encoding="UTF-8").read())

config = {}

apps = {
    "блокнот": "C:\\Windows\\System32\\notepad.exe",
    "калькулятор": "C:\\Windows\\System32\\calc.exe",
    "проводник": "C:\\Windows\\explorer.exe",
    "steam": "C:\\Program Files (x86)\\Steam\\steam.exe",
    "obsidian": "C:\\Users\\pyotr\\AppData\\Local\\Programs\\obsidian\\obsidian.exe",
    "браузер": "C:\\Users\\pyotr\\AppData\\Local\\Programs\\Opera GX\\opera.exe",
    "minecraft": "C:\\XboxGames\\Minecraft Launcher\\Content\\Minecraft.exe",
    "telegram": "C:\\Users\\pyotr\\AppData\\Roaming\\Telegram Desktop\\Telegram.exe",
    "discord": "C:\\Users\\pyotr\\AppData\\Local\\Discord\\app-1.0.9152\\Discord.exe",
    "яндекс музыка": "C:\\Users\\pyotr\\AppData\\Local\\Programs\\YandexMusic\\Яндекс Музыка.exe",
    # Add more applications here
}


def speak(text: str):
    """Говорит слова"""
    engine.say(text)
    engine.runAndWait()


def load_config():
    """Загружает настройки ассистента."""
    global config
    try:
        with open("config.json", "r", encoding="utf-8") as file:
            config = json.load(file)
    except FileNotFoundError:
        config = {"user_name": "Пользователь", "assistant_name": "Ассистент"}


def save_config():
    """Сохраняет текущие настройки в файл."""
    with open("config.json", "w", encoding="utf-8") as file:
        json.dump(config, file, ensure_ascii=False, indent=4)


def play(phrase: str):
    """Воспроизводит записанные речи."""
    filename = f"sound\\jarvis-remake\\"

    if phrase == "greet":  # for py 3.8
        filename += f"greet{random.choice([1, 2, 3])}.wav"
    elif phrase == "ok":
        filename += f"ok{random.choice([1, 2, 3, 4])}.wav"
    elif phrase == "joke":
        filename += f"joke{random.choice([1, 2, 3, 4, 5])}.wav"
    elif phrase == "not_found":
        filename += "not_found.wav"
    elif phrase == "thanks":
        filename += "thanks.wav"
    elif phrase == "run":
        filename += "run.wav"
    elif phrase == "stupid":
        filename += "stupid.wav"
    elif phrase == "ready":
        filename += "ready.wav"
    elif phrase == "off":
        filename += "off.wav"
    elif phrase == "fnaf":
        filename += "fnaf.wav"

    mixer.Sound(filename).play()


def open_website(url: str):
    """Открывает заготовленные вебсайты."""
    webbrowser.open(url)
    speak(f"Открываю {url.split('/')[2]}")


def tell_time():
    """Говорит время."""
    time_now = datetime.datetime.now()
    current_time = time_now.strftime("%H:%M:%S")
    speak(f"Сейчас {current_time}")


def calculate(expression: str):
    """Решает простейшие операции с числами."""
    try:
        result = eval(expression)
        speak(f"Результат {expression} равен {result}")
    except Exception as e:
        speak("Извините, я не могу это посчитать.")


def close_app():
    """Закрывает приложение."""
    keyboard.send("alt+f4")


def search_web(query: str):
    """Ищет в браузере."""
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speak(f"Ищу {query} в Google")


def weather(city: str):
    """Говорит погоду по городу."""
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={appid}&units=metric'

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temperature = data['main']['temp']
            weather_description = data['weather'][0]['description']
            wind_speed = data['wind']['speed']
            pressure = int(data['main']['pressure'] / 1.333)  # Из гПА в мм рт.ст.
            print(f'Погода в городе {city.title()}: {temperature}°C, {weather_description}.')
            speak(f'''Погода в городе {city}: {round(temperature)}° по Цельсию, {weather_type[weather_description]}.
            Скорость ветра составляет {str(wind_speed)} метров в секунду.
            Давление {str(pressure)} миллиметров ртутного столба''')
        else:
            speak(f'Город {city} не найден')
    except:
        speak(
            "Произошла ошибка работы модуля \"Погода\". Подробности в терминале. Возможно вы не подключены к интернету")
        traceback.print_exc()


def open_app(app_name: str):
    """Открывает приложения по названию."""
    app_name = app_name.lower()
    if app_name in apps:
        subprocess.Popen([apps[app_name]])
        speak(f"Открываю {app_name}")
    else:
        speak(f"Извините, я не знаю, как открыть {app_name}")


def volume_down(quantity: str):
    """Уменьшает громкость на какое-то значение."""
    try:
        for key, val in numbers.items():
            if val == quantity:
                quantity = int(key)
        for _ in range(round(quantity / 2)):
            keyboard.send("volume down")
    except TypeError as e:
        speak(f"Ошибка {e}. Повторите пожалуйста попытку")


def volume_up(quantity: str):
    """Увеличивает громкость на какое-то значение."""
    try:
        for key, val in numbers.items():
            if val == quantity:
                quantity = int(key)
        for _ in range(round(quantity / 2)):
            keyboard.send("volume up")
    except TypeError as e:
        speak(f"Ошибка {e}. Повторите пожалуйста попытку")


def volume_mute():
    """Выключает и включает звук."""
    keyboard.send("volume mute")


# def brightness_down(quantity):
#     for key, val in numbers.items():
#         if val == quantity:
#             quantity = int(key)
#     for _ in range(round(quantity / 10)):
#         keyboard.send("brightness down")
#
#
# def brightness_up(quantity):
#     for key, val in numbers.items():
#         if val == quantity:
#             quantity = int(key)
#     for _ in range(round(quantity / 10)):
#         keyboard.send("brightness up")

# Загружаем конфиг при старте
load_config()
