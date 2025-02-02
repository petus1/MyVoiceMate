import os
import fnmatch


def find_exe_files(start_dir, output_file):
    exe_files = []

    # Проходим по всем директориям и поддиректориям
    for dirpath, dirnames, filenames in os.walk(start_dir):
        for filename in fnmatch.filter(filenames, '*.exe'):
            # Сохраняем путь к файлу
            full_path = os.path.join(dirpath, filename)
            exe_files.append(full_path)

    # Записываем результаты в файл
    with open(output_file, 'w', encoding="UTF-8") as f:
        for file in exe_files:
            f.write(file + '\n')

    print(f"Найдено {len(exe_files)} .exe файлов. Результаты сохранены в '{output_file}'.")


# Укажите директорию для поиска и имя выходного файла
start_directory = "C:\\"  # Замените на нужный путь
output_filename = "exe_files.txt"

find_exe_files(start_directory, output_filename)
