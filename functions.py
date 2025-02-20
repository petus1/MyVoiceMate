import speech_recognition as sr  # Распознавание речи online
import pyttsx3  # Синтез речи

import webbrowser  # Открытие вкладок браузера
import datetime
import subprocess  # Запуск новых процессов
from pygame import mixer
import requests
import keyboard
import random  # Генератор случайных чисел
import json  # Работа с данными в формате JSON

engine = pyttsx3.init()
mixer.init()

appid = "b8674996d882d71cf243358cf5634257"

weather_type = json.loads(open('weather_type.json', encoding="UTF-8").read())
commands = json.loads(open('commands.json', encoding="UTF-8").read())
numbers = json.loads(open('numbers.json', encoding="UTF-8").read())

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


def listen():
    """Слушает речь. Прошлая библиотека"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio, language="ru-RU")
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        print("Could not request results; check your network connection.")
        return None


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
    speak(f"Открываю {url.split("/")[2]}")


def tell_time():
    """Говорит время."""
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
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

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        weather_description = data['weather'][0]['description']
        print(f'Погода в городе {city}: {temperature}°C, {weather_description}.')
        speak(f'Погода в городе {city}: {round(temperature)}° по цельсию, {weather_type[weather_description]}.')
    else:
        speak('Город не найден или произошла ошибка.')


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
    for key, val in numbers.items():
        if val == quantity:
            quantity = int(key)
    for _ in range(round(quantity / 2)):
        keyboard.send("volume down")


def volume_up(quantity: str):
    """Увеличивает громкость на какое-то значение."""
    for key, val in numbers.items():
        if val == quantity:
            quantity = int(key)
    for _ in range(round(quantity / 2)):
        keyboard.send("volume up")


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
