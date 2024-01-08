import time
import os
import sqlite3
import info

conn = sqlite3.connect('database.sqlite')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS keys (
        service TEXT,
        key TEXT
    )
''')

services = ['aws_text']

for service in services:
    c.execute("SELECT service FROM keys WHERE service =?", (service,))
    row = c.fetchone()
    if not row:
        c.execute("INSERT INTO keys (service) VALUES (?)", (service,))
c.execute("SELECT service FROM keys WHERE service =?", ("prefix",))
row = c.fetchone()
if not row:
    c.execute("INSERT OR IGNORE INTO keys (service, key) VALUES (?, ?)", ("prefix", "!"))
c.execute("SELECT service FROM keys WHERE service =?", ("aws_status",))
row1 = c.fetchone()
if not row1:
    c.execute("INSERT OR IGNORE INTO keys (service, key) VALUES (?, ?)", ("aws_status", "off"))
conn.commit()


def cc():
    os.system('cls' if os.name == 'nt' else 'clear')


requirements = [
    "pip",
    "pycryptodome",
    "termcolor",
    "pyrogram",
    "TgCrypto",
    "requests",
    "gTTS",
    "apscheduler",
    "colorama"
]


def download_requirements():
    print('Please wait...')
    import subprocess
    subprocess.run(['pip', 'install', 'tqdm', '-U', '-q'], check=True)
    from tqdm import tqdm
    cc()
    libraries = subprocess.run(["pip", "list"], check=True, capture_output=True, text=True).stdout
    for lib in tqdm(requirements, desc="Installing libraries..."):
        if lib not in libraries:
            subprocess.run(['pip', 'install', lib, '-U', '-q'], check=True)
        else:
            pass
    cc()


def update_userbot():
    from helps.scripts import restart
    import requests
    from tqdm import tqdm
    print("Поиск обновлений...")
    ver = requests.get("https://raw.githubusercontent.com/Timka4959000/TimkaUserBot/main/info.py")
    ver = ver.text.replace('version = "', "").replace('"', "")
    if ver == info.version:
        print("Обновления не найдены")
        return
    else:
        plugins_files = ["bot.py", "change_prefix.py", "help.py", "modules_actions.py", "ping.py", "restart.py",
                         "send_log.py", "~_###_zzz_logo.py"]
        for plugin in tqdm(plugins_files, desc="Update plugins..."):
            new_code = requests.get(
                f"https://raw.githubusercontent.com/Timka4959000/TimkaUserBot/main/plugins/{plugin}").text
            old_code = open(f"plugins/{plugin}", "w+")
            if old_code.read() == new_code:
                pass
            else:
                old_code.write(new_code)
                old_code.close()

        system_files = ["main.py", "info.py", "helps/get_prefix.py", "helps/modules.py", "help/scripts.py"]

        for file in tqdm(system_files, desc="Update system..."):
            new_code = requests.get(f"https://raw.githubusercontent.com/Timka4959000/TimkaUserBot/main/{file}").text
            old_code = open(file, "w+")
            if old_code.read() == new_code:
                pass
            else:
                old_code.write(new_code)
                old_code.close()

        print("Update successfully!")
        time.sleep(3)
        cc()
        restart()


def logging_setup():
    import logging

    logging.basicConfig(level=logging.INFO, filename="log.log", filemode="a+")


def login_client():
    from pyrogram import Client, idle
    from pyrogram.enums import ParseMode
    from helps.scripts import get_lang

    if not os.path.isfile("restart.txt"):
        if os.path.isfile("TimkaUserBot.session-journal"):
            os.remove("TimkaUserBot.session-journal")

    if not os.path.isfile("lang.txt"):
        while True:
            lang_code = input("Select language // Выберите язык (ru/en): ")
            if lang_code not in ['en', 'ru']:
                cc()
                print("incorrect answer // некоректный ответ")
                time.sleep(3)
                cc()
            else:
                write_lang = open("lang.txt", "w")
                write_lang.write(lang_code)
                write_lang.close()
                break
        if not lang_code:
            lang_code = get_lang()

    if not os.path.isfile("TimkaUserBot.session"):
        if lang_code == 'ru':
            api_id = input("Введите API ID: ")
            api_hash = input("Введите API Hash: ")
        else:
            api_id = input("Enter API ID: ")
            api_hash = input("Enter API Hash: ")

        app = Client(
            name="TimkaUserBot",
            api_hash=api_hash,
            api_id=api_id,
            device_model="POCO X3 PRO",
            system_version="ANDROID 13",
            app_version="10.2.9",
            lang_code=lang_code,
            plugins=dict(root="plugins"),
            parse_mode=ParseMode.HTML
        )
    else:
        app = Client(
            name="TimkaUserBot",
            plugins=dict(root="plugins")
        )

    with app:
        if not os.path.isfile("restart.txt"):
            pass
        else:
            f = open("restart.txt", "r")
            chat_id = f.read()
            f.close()

            os.remove("restart.txt")

            try:
                if lang_code == "en":
                    app.send_message(chat_id, "<b>TimkaUserBot successfully rebooted</b>")
                else:
                    app.send_message(chat_id, "<b>TimkaUserBot успешно перезагружен</b>")
            except Exception as e:
                if lang_code == "en":
                    app.send_message("me", f"<b>TimkaUserBot rebooted successfully, but an error occurred while "
                                           f"sending a message\n\nLOG:</b> {e}")
                else:
                    app.send_message("me", f"<b>TimkaUserBot успешно перезагружен, но произошла ошибка при отправке "
                                           f"сообщения\n\nLOG:</b> {e}")

    app.start()
    idle()
    app.stop()


if __name__ == "__main__":
    if not os.path.isfile("restart.txt"):
        download_requirements()
        update_userbot()
    logging_setup()
    login_client()
