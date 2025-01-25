import pyttsx3


class bot:
    bot_name_ru = ""
    bot_name_en = ""


if __name__ == "__main__":
    trex = bot()
    trex.bot_name_ru = "Тирекс"
    trex.bot_name_en = "Trex"


def speak(my_bot, text):
    print(my_bot.bot_name_ru, " говорит: ", text)
    engine.say(text)
    engine.runAndWait()


if __name__ == "__main__":
    trex = bot()
    trex.bot_name_ru = "Тирекс"
    trex.bot_name_en = "Trex"

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    # Прослушивание голосов, доступных в ОС
    i = 0
    for voice in voices:
        engine.setProperty('voice', voices[i].id)
        print('Имя: %s' % voice.name)
        print('ID: ', i)
        speak(trex, "1")
        print('--------------------')
        i = i + 1
