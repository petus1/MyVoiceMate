from the_command_handler import *  # Импорт обработчика команд и функций
from logger import logger

import speech_recognition as sr  # Распознавание речи online
from vosk import Model, KaldiRecognizer  # Распознавание речи offline

import argparse  # Парсинг аргументов командной строки
import sys  # Системные функции и обработка ошибок
import sounddevice as sd  # Работа с аудиоустройствами
import queue  # Очередь для обработки потоков
import json

# Очередь для обработки аудиопотока
q = queue.Queue()


# Класс ассистента
class Bot:
    bot_name_ru = ""
    bot_name_en = ""
    city = ""
    language = ""


# Приветственное сообщение при запуске программы
def greetings():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 6:
        speak(f"Доброй ночи! Я - {my_voice_mate.bot_name_ru}, твой голосовой помощник. Чем могу помочь?")
    elif 6 <= hour < 12:
        speak(f"Доброе утро! Я - {my_voice_mate.bot_name_ru}, твой голосовой помощник. Чем могу помочь?")
    elif 12 <= hour < 18:
        speak(f"Добрый день! Я - {my_voice_mate.bot_name_ru}, твой голосовой помощник. Чем могу помочь?")
    else:
        speak(f"Добрый вечер! Я - {my_voice_mate.bot_name_ru}, твой голосовой помощник. Чем могу помочь?")


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


def check_internet() -> bool:
    """Проверяет доступность интернета путём запроса к Google."""
    try:
        requests.get("https://www.google.com", timeout=2)
        return True
    except requests.RequestException:
        return False


def callback(indata, frames, time, status):
    """Обработчик потока аудиоданных. Полученные данные помещает в очередь."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


def recognize_online() -> str:
    """Распознавание речи онлайн через Google API."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening online...")
        recognizer.adjust_for_ambient_noise(source)  # Подстройка под окружающий шум
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio, language="ru-RU")
    except sr.UnknownValueError:
        print("Не удалось распознать речь.")
    except sr.RequestError:
        print("Ошибка запроса к сервису Google.")
    return ""


def recognize_offline(model: Model) -> str:
    """Распознавание речи офлайн с использованием Vosk."""
    recognizer = KaldiRecognizer(model, 16000)
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16", channels=1, callback=callback):
        print("Listening offline...")
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):  # Завершение обработки при полном распознавании
                result = json.loads(recognizer.Result())
                text = result.get("text", "")
                if text:
                    return text


def listen() -> str:
    """Определяет способ распознавания речи в зависимости от наличия интернета."""
    if check_internet():
        return recognize_online()
    else:
        model = Model(lang="ru")
        return recognize_offline(model)


def main():
    """Главная функция программы, обрабатывающая голосовые команды."""
    parser = argparse.ArgumentParser(description="Speech recognition script")
    parser.add_argument("-d", "--device", type=int_or_str, help="ID аудиоустройства")
    parser.add_argument("-r", "--samplerate", type=int, help="Частота дискретизации")
    parser.add_argument("-m", "--model", type=str, default="ru", help="Языковая модель (например, ru, en-us)")
    args = parser.parse_args()

    try:
        model = Model(lang=args.model)
        logger.info("Голосовой ассистент запущен и готов к работе")
        while True:
            command = listen()
            if command:
                print(f"Вы сказали: {command}")
                command_handler(command.lower())  # Обработка распознанной команды
    except KeyboardInterrupt:
        logger.info("Пользователь прервал работу ассистента")
        print("\nВыход...")
    except Exception as e:
        logger.error(f"Критическая ошибка в main: {e}")
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    # Модель для offline распознавания
    model = Model(lang="ru")  # куда скачивается C:\Users\<USER>\.cache\vosk

    # Персонализация бота
    my_voice_mate = Bot()
    my_voice_mate.bot_name_ru = "Петус"
    my_voice_mate.bot_name_en = "Petus"
    my_voice_mate.city = "Москва"
    my_voice_mate.language = "ru"

    greetings()
    main()
