from colorama import Fore, Style
import os
from info import version
from helps.get_prefix import get_prefix
from helps.scripts import get_lang

lang = get_lang()
prefix = get_prefix()

os.system('cls' if os.name == 'nt' else 'clear')
print(Fore.MAGENTA + " _____  _             _            _   _                   ____          _   ")
print(Fore.LIGHTCYAN_EX + "|_   _|(_) _ __ ___  | | __  __ _ | | | | ___   ___  _ __ | __ )   ___  | |_ ")
print(Fore.MAGENTA + "  | |  | || '_ ` _ \ | |/ / / _` || | | |/ __| / _ \| '__||  _ \  / _ \ | __|")
print(Fore.LIGHTCYAN_EX + "  | |  | || | | | | ||   < | (_| || |_| |\__ \|  __/| |   | |_) || (_) || |_ ")
print(Fore.MAGENTA + "  |_|  |_||_| |_| |_||_|\_\ \__,_| \___/ |___/ \___||_|   |____/  \___/  \__|\n")
if lang == "ru":
    print(Fore.LIGHTCYAN_EX + f"Текущий префикс: [{prefix}]")
    print(Fore.MAGENTA + f"Версия юзербота: {version}\n")
    print(Fore.LIGHTCYAN_EX + f"Для получения помощи - {prefix}help")
    print(Fore.MAGENTA + f"Для получения информации о юзерботе - {prefix}bot")
    print(Fore.LIGHTCYAN_EX + f"Для получения пинга - {prefix}ping")
    print(Style.RESET_ALL)
else:
    print(Fore.LIGHTCYAN_EX + f"Current prefix: [{prefix}]")
    print(Fore.MAGENTA + f"Userbot version: {version}\n")
    print(Fore.LIGHTCYAN_EX + f"For help - {prefix}help")
    print(Fore.MAGENTA + f"To get info about the userbot - {prefix}bot")
    print(Fore.LIGHTCYAN_EX + f"To get ping - {prefix}ping")
    print(Style.RESET_ALL)
