from the_command_handler import *  # Импорт обработчика команд и функций

import speech_recognition as sr  # Распознавание речи online
from vosk import Model, KaldiRecognizer  # Распознавание речи offline

import argparse  # Парсинг аргументов командной строки
import sys  # Системные функции и обработка ошибок
import sounddevice as sd  # Работа с аудиоустройствами
import queue  # Очередь для обработки потоков

# Очередь для обработки аудиопотока
q = queue.Queue()


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
                return result.get("text", "")


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
        while True:
            command = listen()
            if command:
                print(f"Вы сказали: {command}")
                command_handler(command.lower())  # Обработка распознанной команды
    except KeyboardInterrupt:
        print("\nВыход...")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    model = Model(lang="ru")
    recognize_offline(model)
    speak("Голосовой ассистент запущен!")
    main()
