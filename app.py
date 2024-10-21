import streamlit as st
from telethon import TelegramClient
import os
import asyncio

# Ваши параметры для Telethon
api_id = '22328650'
api_hash = '20b45c386598fab8028b1d99b63aeeeb'
channel_id = '-1002396135016'

async def send_video_to_channel(video_path, channel_id, phone=None, code=None):
    client = TelegramClient('session_name', api_id, api_hash)
    
    try:
        await client.connect()
        if not await client.is_user_authorized():
            if phone and code:
                await client.sign_in(phone, code)
            else:
                raise Exception("Необходимо пройти авторизацию")

        # Отправка видео в канал
        await client.send_file(channel_id, video_path)
        return True
    except Exception as e:
        st.error(f"Ошибка при отправке видео: {str(e)}")
        return False
    finally:
        await client.disconnect()

# Функция для запуска асинхронной задачи в Streamlit
def run_async_task(task):
    loop = asyncio.new_event_loop()  # Создаем новый событийный цикл
    asyncio.set_event_loop(loop)  # Устанавливаем его как текущий
    result = loop.run_until_complete(task)
    loop.close()
    return result

# Интерфейс Streamlit
st.title("Загрузка и отправка видео в Telegram канал")

uploaded_files = st.file_uploader("Загрузите видео", type=['mp4', 'mov', 'avi'], accept_multiple_files=True)

if 'videos' not in st.session_state:
    st.session_state['videos'] = []

if uploaded_files:
    for uploaded_file in uploaded_files:
        # Сохраняем видео временно на сервере
        video_path = os.path.join('temp_videos', uploaded_file.name)
        with open(video_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        st.session_state['videos'].append(video_path)

    st.success("Видео успешно загружено!")

# Отображение списка видео
st.header("Список загруженных видео")
if st.session_state['videos']:
    for video in st.session_state['videos']:
        st.write(video)

# Кнопка отправки видео в канал
if st.button("Отправить видео в Telegram канал"):
    phone = st.text_input('Введите ваш номер телефона для авторизации:', key='phone_input')
    code = st.text_input('Введите код из SMS:', key='code_input')
    
    if st.session_state['videos']:
        with st.spinner("Отправка видео..."):
            for video_path in st.session_state['videos']:
                st.info(f"Отправка {video_path} в канал...")
                # Отправляем видео в Telegram канал
                result = run_async_task(send_video_to_channel(video_path, channel_id, phone, code))
                if result:
                    st.success(f"Видео {video_path} успешно отправлено!")
                else:
                    st.error(f"Не удалось отправить видео {video_path}")
    else:
        st.error("Нет загруженных видео для отправки.")
