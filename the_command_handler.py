from functions import *  # Импорт всех функций ГА


# обработчик голосовых команд
def command_handler(command):
    if command:
        if config["assistant_name"].lower() in command:
            speak(f"Слушаю вас, {config['user_name']}.")

        elif "зови меня теперь" in command:
            new_name = command.replace("зови меня теперь", "").strip()
            config["user_name"] = new_name
            save_config()
            load_config()  # Перезагружаем настройки
            speak(f"Теперь я буду обращаться к вам, {new_name}.")

        elif "измени имя ассистента" in command:
            new_assistant_name = command.replace("измени имя ассистента на", "").strip()
            config["assistant_name"] = new_assistant_name
            save_config()
            load_config()  # Перезагружаем настройки
            speak(f"Теперь меня зовут {new_assistant_name}.")

        elif "привет" in command:
            speak("Привет! Как дела?")

        elif "спасибо" in command or "ты молодец" in command:
            play("thanks")

        elif "ты плохой" in command or "плохо работаешь" in command:
            play("stupid")

        elif "как дела" in command:
            speak("У меня все хорошо, спасибо! А у тебя?")

        elif "выключение питания" in command or "выключении питания" in command:
            speak("До свидания!")
            quit()  # Выход из программы

        elif "хорошо" in command:
            speak("Ну это хорошо")

        elif "отлично" in command:
            speak("Это очень хорошо!")

        elif "фредди" in command:
            play("fnaf")

        elif "погода" in command:
            city = command.replace("погода", "").strip()
            city = city.split()[-1]
            print(city)
            weather(city)

        elif "расскажи шутку" in command or "скажи шутку" in command:
            play("joke")

        elif "следующая" in command or "следующее" in command or "следующая песня" in command or "следующая музыка" in command:
            keyboard.send("next track")  # следующий трек

        elif "предыдущая" in command or "предыдущая песня" in command or "предыдущая музыка" in command:
            keyboard.send("previous track")  # предыдущий трек

        elif "пауза" in command or "стоп" in command or "воспроизведение" in command or "продолжай" in command:
            keyboard.send("play/pause media")  # pause/play для всех медиа

        elif "открой" in command:
            if "гугл" in command:
                open_website("https://www.google.com")
            elif "youtube" in command:
                open_website("https://www.youtube.com")
            else:
                app_name = command.replace("открой", "").strip()
                open_app(app_name)

        elif "сколько время" in command or "который час" in command or "сколько времени" in command:
            tell_time()

        elif "посчитай" in command:
            expression = command.replace("посчитай", "").strip()
            calculate(expression)

        elif "закрой программу" in command or "выключи это" in command or "закрой приложение" in command:
            close_app()

        elif "послушаем музыку" in command or "яндекс музыка" in command:
            open_app("яндекс музыка")
            # open_website("https://music.youtube.com/watch?playlist=LM")

        elif "найди" in command or "найти" in command:
            query = command.replace("найди", "").strip()
            query = query.replace("найти", "").strip()
            search_web(query)

        elif "стоп" in command or "хватит" in command:
            speak("Выход из режима ожидания.")

        elif "понизь громкость на" in command or "убавь громкость на" in command or "уменьши громкость на" in command:
            quantity = command.replace("понизь громкость на", "").strip()
            quantity = quantity.replace("убавь громкость на", "").strip()
            quantity = quantity.replace("уменьши громкость на", "").strip()
            volume_down(quantity)

        elif "повысь громкость на" in command or "увеличь громкость на" in command:
            quantity = command.replace("повысь громкость на", "").strip()
            quantity = quantity.replace("увеличь громкость на", "").strip()
            volume_up(quantity)

        elif "отключи громкость" in command or "включи громкость" in command or "выключи звук" in command:
            volume_mute()

        # elif "понизь яркость на" in command or "убавь яркость на" in command or "уменьши яркость на" in command:
        #     quantity = command.replace("понизь яркость на", "").strip()
        #     quantity = quantity.replace("убавь яркость на", "").strip()
        #     quantity = quantity.replace("уменьши яркость на", "").strip()
        #     brightness_down(quantity)
        # elif "повысь яркость на" in command or "увеличь яркость на" in command:
        #     quantity = command.replace("повысь яркость на", "").strip()
        #     quantity = quantity.replace("увеличь яркость на", "").strip()
        #     brightness_up(quantity)
