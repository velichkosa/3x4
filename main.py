from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import yaml

import remove_bg
import scale
import os

remove_bg = remove_bg.remove_bg

with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

bot = Bot(token=config['token'])
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.chat.id, "Привет Иван! Прикрепи сюда фото".
                           format(message.from_user))


@dp.message_handler(content_types=['photo'])
async def text_recognition(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    delete_message = await bot.send_message(chat_id, 'Ща замучу...'.
                                            format(message.from_user))
    src = f'files/{message.chat.id}/'

    await message.photo[-1].download(destination_file=src + 'temp.jpg')

    remove_bg(src + 'temp.jpg', src + 'clrbg.jpg')
    scale.scale_cv2(src + 'clrbg.jpg', src)
    os.remove(src + 'clrbg.jpg')
    photo = open(src + 'result.jpg', 'rb')  # rb - чтение байтов, wb - запись байтов.

    await bot.send_photo(chat_id, photo)

    # image_text = textr.recognition(src, 'temp.jpg', language)
    # db.to_mongo(user_id, image_text, 'update_temp')
    # await bot.send_message(chat_id, text=image_text, reply_markup=kb.inline_text_kb)
    # await bot.delete_message(chat_id, delete_message.message_id)


# remove_bg = remove_bg.remove_bg
# remove_bg('test3.jpg', 'clrbg.jpg')
# scale.scale_cv2('clrbg.jpg')
# os.remove('clrbg.jpg')


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
