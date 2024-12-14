import vosk
import pyttsx3
import pyaudio
import os
import json
from datetime import datetime
import random

# Инициализация синтеза речи
engine = pyttsx3.init()
engine.setProperty("voice", "ru")  # Русский голос

def speak(text):
    """Произнести текст"""
    engine.say(text)
    engine.runAndWait()

# Путь к модели Vosk
MODEL_PATH = r"C:\Users\Abdula\Documents\vosk-model-small-ru-0.22"

# Проверяем, есть ли модель
if not os.path.exists(MODEL_PATH):
    print("Модель не найдена! Скачайте её с сайта Vosk и поместите в текущую директорию.")
    exit(1)

# Инициализация модели
model = vosk.Model(MODEL_PATH)
recognizer = vosk.KaldiRecognizer(model, 16000)

# Настраиваем микрофон
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

# Функция обработки команд
def handle_command(command):
    """Обработать команды пользователя"""
    command = command.lower()

    # Приветствие
    if "привет" in command:
        responses = ["Привет!", "Здравствуйте!", "Как настроение?"]
        speak(random.choice(responses))

    # Время
    elif "время" in command:
        now = datetime.now()
        speak(f"Сейчас {now.hour} часов {now.minute} минут.")

    # Выключение компьютера
    elif "выключи компьютер" in command:
        speak("Выключаю компьютер. До свидания!")
        os.system("shutdown /s /t 1")

    # Умный ответ
    elif "как тебя зовут" in command:
        speak("Меня зовут ассистент. А вас?")

    elif "как дела" in command:
        responses = ["У меня всё отлично, спасибо! А у вас?", "Работаю, как всегда!", "Хорошо, что вы спросили!"]
        speak(random.choice(responses))

    elif "расскажи анекдот" in command:
        jokes = [
            "Почему программисты не ходят в лес? Потому что боятся заблудиться в деревьях.",
            "Девушка на свидании: 'И что ты можешь мне предложить?' Парень: 'Программу для оптимизации наших отношений.'",
            "Если долго сидеть за компьютером, можно стать виндоузером."
        ]
        speak(random.choice(jokes))

    # Завершение работы
    elif "стоп" in command or "выход" in command:
        speak("До свидания! Было приятно поговорить.")
        return False

    # Команда не распознана
    else:
        speak("Извините, я не понял вашу команду.")

    return True

# Основной цикл
print("Ассистент слушает... (нажмите Ctrl+C для выхода)")
try:
    while True:
        data = stream.read(4000, exception_on_overflow=False)

        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            command = result.get("text", "").lower()
            print(f"Вы сказали: {command}")

            if not handle_command(command):
                break
except KeyboardInterrupt:
    print("Выход из программы...")
finally:
    stream.stop_stream()
    stream.close()
    audio.terminate()
