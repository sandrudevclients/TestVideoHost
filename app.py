import streamlit as st
from telethon.sync import TelegramClient
from telethon.tl.types import DocumentAttributeFilename
import asyncio

# Указываем API ID и Hash
api_id = '22328650'
api_hash = '20b45c386598fab8028b1d99b63aeeeb'

# Юзернейм канала
channel_username = 'testchannelparso'

# Асинхронная функция для получения всех файлов
async def async_get_files_from_channel(client):
    entity = await client.get_entity(channel_username)
    files = []
    async for message in client.iter_messages(entity):
        if message.media and hasattr(message.media, 'document'):
            for attribute in message.media.document.attributes:
                if isinstance(attribute, DocumentAttributeFilename):
                    files.append((attribute.file_name, message))
    return files

# Асинхронная функция для скачивания файла
async def async_download_file(client, message, file_name):
    return await message.download_media(file=file_name)

# Синхронная обертка для получения файлов
def get_files_from_channel():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    with TelegramClient('session_name', api_id, api_hash) as client:
        return loop.run_until_complete(async_get_files_from_channel(client))

# Синхронная обертка для скачивания файла
def download_file(message, file_name):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    with TelegramClient('session_name', api_id, api_hash) as client:
        return loop.run_until_complete(async_download_file(client, message, file_name))

# Интерфейс Streamlit
st.title('File Downloader from Telegram Channel')

# Получаем список файлов
files = get_files_from_channel()

if files:
    # Выбор файла для скачивания
    file_to_download = st.selectbox("Select a file to download:", [f[0] for f in files])

    if st.button('Download'):
        # Поиск выбранного сообщения
        selected_message = next((f[1] for f in files if f[0] == file_to_download), None)

        if selected_message:
            # Скачиваем файл
            file_path = download_file(selected_message, file_to_download)
            if file_path:
                with open(file_path, 'rb') as file:
                    st.download_button(
                        label=f"Download {file_to_download}",
                        data=file,
                        file_name=file_to_download
                    )
else:
    st.write("No files found in the channel.")
