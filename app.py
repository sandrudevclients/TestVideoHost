import streamlit as st
from telethon.sync import TelegramClient
from telethon.tl.types import DocumentAttributeFilename
import os
import asyncio

# Указываем API ID и Hash
api_id = '22328650'
api_hash = '20b45c386598fab8028b1d99b63aeeeb'

# Юзернейм канала
channel_username = 'testchannelparso'

# Создаем клиент
client = TelegramClient('session_name', api_id, api_hash)

# Функция для получения всех файлов из канала
async def async_get_files_from_channel():
    await client.start()
    entity = await client.get_entity(channel_username)
    
    files = []
    async for message in client.iter_messages(entity):
        if message.media and hasattr(message.media, 'document'):
            for attribute in message.media.document.attributes:
                if isinstance(attribute, DocumentAttributeFilename):
                    files.append((attribute.file_name, message))
    return files

def get_files_from_channel():
    # Запускаем асинхронную функцию в event loop
    return asyncio.run(async_get_files_from_channel())

# Стримлит интерфейс
st.title('File Downloader from Telegram Channel')

# Получаем список файлов
files = get_files_from_channel()

if files:
    # Выводим список файлов для выбора
    file_to_download = st.selectbox("Select a file to download:", [f[0] for f in files])

    if st.button('Download'):
        # Ищем выбранное сообщение
        selected_message = next((f[1] for f in files if f[0] == file_to_download), None)

        if selected_message:
            # Скачиваем файл
            file_path = selected_message.download_media(file=file_to_download)
            with open(file_path, 'rb') as file:
                btn = st.download_button(
                    label=f"Download {file_to_download}",
                    data=file,
                    file_name=file_to_download
                )

else:
    st.write("No files found in the channel.")
