<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Голосовой Ассистент</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #1e1b3a;
            color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            flex-direction: column;
        }

        #start {
            padding: 15px 30px;
            font-size: 1.5rem;
            border: none;
            background-color: #6c4fbb;
            color: white;
            border-radius: 8px;
            cursor: pointer;
        }

        #start:hover {
            background-color: #5a3e99;
            transform: scale(1.1);
        }
    </style>
</head>
<body>

    <h1>Голосовой Ассистент</h1>
    <button id="start">Запустить</button>
    
    <script>
        // Функция для синтеза речи
        function speak(text) {
            const utterance = new SpeechSynthesisUtterance(text);
            const voices = window.speechSynthesis.getVoices();
            utterance.voice = voices.find(voice => voice.lang === 'ru-RU') || voices[0];
            window.speechSynthesis.speak(utterance);
        }

        // Функция для распознавания речи
        function startRecognition() {
            const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = 'ru-RU'; // Устанавливаем язык на русский
            recognition.continuous = false;
            recognition.interimResults = true;

            recognition.onstart = function() {
                console.log("Голосовое распознавание начато...");
            };

            recognition.onerror = function(event) {
                console.error("Ошибка распознавания:", event.error);
            };

            recognition.onresult = function(event) {
                const transcript = event.results[0][0].transcript;
                console.log("Распознанный текст: ", transcript);
                speak("Вы сказали: " + transcript); // Отправляем обратно ответ
            };

            recognition.start(); // Запуск распознавания
        }

        // Обработчик для кнопки старта
        document.getElementById('start').addEventListener('click', function() {
            speak('Здравствуйте! Я готов вас слушать.');
            startRecognition(); // Запуск распознавания
        });
    </script>
</body>
</html>
