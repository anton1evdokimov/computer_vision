import telebot
from openai import OpenAI
from gtts import gTTS
import os

# Токен телеграм-бота @Anton1EvdokimovBot
TOKEN = '7106183236:AAEK9zS1TTnX-ciQB93mpp6UoY2HkHrOtwE'
bot = telebot.TeleBot(TOKEN)

# Инициализация клиента API OpenAI с API ключом
client = OpenAI(
    api_key="sk-eojihWMYuwlwO4oNjNMX8DbkkkBtLg7I", # sk-MU1aRWtUZbVJzxQVlDNQEngmU6ZwYFS8
    base_url="https://api.proxyapi.ru/openai/v1"
)

# Словарь для хранения истории разговора с каждым пользователем
conversation_histories = {}
# Словарь для хранения типа ответа для каждого пользователя
users_with_voice_response = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message, "Привет! Я бот, который может поддержать разговор на любую тему."
    )

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(
        message, "Привет! Чтобы выбрать формат ответа, напишите /voice или /text"
    )

@bot.message_handler(commands=['voice'])
def set_voice_response(message):
    users_with_voice_response[message.chat.id] = True
    bot.send_message(
        message.chat.id, "Понял вас! Теперь я буду тебе отвечать голосовыми сообщениями"
    )

@bot.message_handler(commands=['text'])
def set_text_response(message):
    users_with_voice_response.pop(message.chat.id, None)
    bot.send_message(message.chat.id, "Понял вас! Теперь я буду тебе отвечать текстом")


# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id
    user_input = message.text
    print(f"Get message from userId: {user_id}")

    if user_id not in conversation_histories:
        conversation_histories[user_id] = []

    conversation_history = conversation_histories[user_id]
    # Добавление ввода пользователя в историю разговора
    conversation_history.append({"role": "user", "content": user_input})

    # Отправка запроса в нейронную сеть
    chat_completion = client.chat.completions.create(
      model="gpt-3.5-turbo-1106",
      messages=conversation_history
    )

    # Извлечение ответа нейронной сети
    ai_response_content = chat_completion.choices[0].message.content

    if ai_response_content is not None:
        is_voice_reply = users_with_voice_response.get(message.chat.id)
    
        # ответ на сообщение
        if is_voice_reply:
          # Создаем объект gTTS для преобразования текста в речь
          tts = gTTS(ai_response_content, lang='ru')
          # Создаем временный файл для сохранения аудио
          temp_file = "temp_audio.mp3"
          tts.save(temp_file)
    
          # Отправляем аудио-сообщение пользователю
          with open(temp_file, 'rb') as audio:
              bot.send_voice(message.chat.id, audio)
    
          # Удаляем временный файл
          os.remove(temp_file)
        else:
           bot.reply_to(message, ai_response_content)

    # Добавление ответа нейронной сети в историю разговора
    conversation_history.append({"role": "system", "content": ai_response_content})

print("Бот запущен и готов к работе...")

if __name__ == '__main__':
  bot.infinity_polling()

