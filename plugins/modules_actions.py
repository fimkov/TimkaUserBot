from pyrogram import Client, filters
from helps.modules import add_module, add_command, load_module, commands, upload_module
import os
from helps.get_prefix import get_prefix
from helps.scripts import restart
from helps.scripts import get_lang

prefix = get_prefix()
lang = get_lang()


class Texts_load:
    @staticmethod
    def get_texts():
        return {"error": {
            "ru": f"Помощь: {prefix}help modules",
            "en": f"Help: {prefix}help modules"
        },
            "error 2": {
                "ru": "Файл с названием как у этого модуля уже существует!",
                "en": "A file with the name of this module already exists!"
            },
            "successfully": {
                "ru": " успешно установлен",
                "en": " successfully installed"
            },
            "reload": {
                "ru": "<b>Перезагружаю юзербота...</b>",
                "en": "<b>Rebooting the user bot...</b>"
            }
        }


class Texts_upload:
    @staticmethod
    def get_texts():
        return {"error": {
            "ru": f"Помощь: {prefix}help modules",
            "en": f"Help: {prefix}help modules"
        },
            "notfound": {
                "ru": "Модуль не найден",
                "en": "Module not found"
            },
            "successfully": {
                "ru": " успешно установлен",
                "en": " successfully installed"
            },
            "reload": {
                "ru": "<b>Перезагружаю юзербота...</b>",
                "en": "<b>Rebooting the user bot...</b>"
            }
        }


class Texts_remove:
    @staticmethod
    def get_texts():
        return {
        "error": {
            "ru": f"Помощь: {prefix}help modules",
            "en": f"Help: {prefix}help modules"
        },
            "notfound": {
                "ru": "Модуль не найден",
                "en": "Module not found"
            },
            "successfully": {
                "ru": " успешно удалён",
                "en": " successfully removed"
            },
            "reload": {
                "ru": "<b>Перезагружаю юзербота...</b>",
                "en": "<b>Rebooting the user bot...</b>"
            },
            "error2": {
                "ru": f"Возникла ошибка! Подробнее в логе ({prefix}send_log)",
                "en": f"An error has occurred! Read more in the log ({prefix}send_log)"
            }
        }


@Client.on_message(filters.command(["lmodule", "load_module", "lm"], prefix) & filters.me)
async def lmodule(client, message):
    text_versions = Texts_load.get_texts()
    if not message.reply_to_message:
        try:
            link = message.command[1]
        except:
            await message.edit(text_versions['error'][lang])
            return

        info = load_module(link)

        if os.path.isfile(f"plugins/{info[0]}"):
            await message.edit(text_versions['error 2'][lang])
            return

        f = open(f"plugins/{info[0]}", "w+", encoding='utf-8')
        f.write(info[1])
        f.close()

        await message.edit(info[0].replace('.py', '') + text_versions['successfully'][lang])
        await message.reply(text_versions["reload"][lang])
        await restart(message=message)
    else:
        await client.download_media(message.reply_to_message.document, file_name='plugins/')
        await message.edit("Модуль" + text_versions['successfully'][lang])
        await message.reply(text_versions["reload"][lang])
        await restart(message=message)


@Client.on_message(filters.command(["umodule", "upload_module", "um"], prefix) & filters.me)
async def uplmodule(client, message):
    text_versions = Texts_upload.get_texts()
    try:
        name = message.command[1]
    except IndexError:
        await message.edit(text_versions['error'][lang])
        return

    filename = upload_module(name)
    if filename == "Module not found":
        await message.edit(text_versions['notfound'][lang])

    module_commands = commands[name]
    result = ""
    for command_name, help_command in module_commands.items():
        result = result + f"<code>{command_name}</code> - <i>{help_command}</i>\n"

    await client.send_document(message.chat.id, document=open(filename, "rb"), file_name=name + ".py",
                               caption=f"<b>{name}</b>\n\n{result}")
    await message.delete()


@Client.on_message(filters.command(["rmodule", "remove_module", "rm"], prefix) & filters.me)
async def rmmodule(client, message):
    text_versions = Texts_remove.get_texts()
    try:
        name = message.command[1]
    except IndexError:
        await message.edit(text_versions['error'][lang])
        return

    result = upload_module(name)
    if result == "Module not found":
        await message.edit(text_versions['notfound'][lang])
        return

    elif result == "error":
        await message.edit(text_versions['error2'][lang])
        return

    else:
        await message.edit(name + text_versions['successfully'][lang])
        await message.reply(text_versions['reload'][lang])
        await restart(message)


if lang == "ru":
    add_module("modules", __file__)
    add_command("modules", f"{prefix}load_module [raw ссылка/в ответ на файл с модулем]", "устанавливает модуль")
    add_command("modules", f"{prefix}lmodule [raw ссылка/в ответ на файл с модулем]", "устанавливает модуль")
    add_command("modules", f"{prefix}lm [raw ссылка/в ответ на файл с модулем]", "устанавливает модуль")
    add_command("modules", f"{prefix}upload_module [имя модуля]", "Отправляет файл модуля в чат")
    add_command("modules", f"{prefix}umodule [имя модуля]", "Отправляет файл модуля в чат")
    add_command("modules", f"{prefix}um [имя модуля]", "Отправляет файл модуля в чат")
    add_command("modules", f"{prefix}remove_module [имя модуля]", "Удаляет модуль")
    add_command("modules", f"{prefix}rmodule [имя модуля]", "Удаляет модуль")
    add_command("modules", f"{prefix}rm [имя модуля]", "Удаляет модуль")
else:
    add_module("modules", __file__)
    add_command("modules", f"{prefix}load_module [raw link/in response to module file]", "installs a module")
    add_command("modules", f"{prefix}lmodule [raw link/in response to module file]", "installs a module")
    add_command("modules", f"{prefix}lm [raw link/in response to module file]", "installs a module")
    add_command("modules", f"{prefix}upload_module [module name]", "sends module file to chat")
    add_command("modules", f"{prefix}umodule [module name]", "sends module file to chat")
    add_command("modules", f"{prefix}um [module name]", "sends module file to chat")
    add_command("modules", f"{prefix}remove_module [module name]", "Delete the module")
    add_command("modules", f"{prefix}rmodule [module name]", "Delete the module")
    add_command("modules", f"{prefix}rm [module name]", "Delete the module")
