# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging

# Импортируем datetime и timetable
import datetime as dt
from lessons import timetable

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request, jsonify
app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}

# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])

def main():
# Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )

# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        sessionStorage[user_id] = {
            'suggests': [
                "Не хочу.",
                "Не буду.",
                "Отстань!",
            ]
        }

        
        res['response']['text'] = convert_timetable()
        res['response']['buttons'] = get_suggests(user_id)
        return

    # Обрабатываем ответ пользователя.
    if req['request']['original_utterance'].lower() in [
        'ладно',
        'куплю',
        'покупаю',
        'хорошо',
    ]:
        # Пользователь согласился, прощаемся.
        res['response']['text'] = 'Слона можно найти на Яндекс.Маркете!'
        return

    # Если нет, то убеждаем его купить слона!
    res['response']['text'] = 'Все говорят "%s", а ты купи слона!' % (
        req['request']['original_utterance']
    )
    res['response']['buttons'] = get_suggests(user_id)

# Функция возвращает две подсказки для ответа.
def get_suggests(user_id):
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    # Убираем первую подсказку, чтобы подсказки менялись каждый раз.
    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    # Если осталась только одна подсказка, предлагаем подсказку
    # со ссылкой на Яндекс.Маркет.
    if len(suggests) < 2:
        suggests.append({
            "title": "Ладно",
            "url": "https://market.yandex.ru/search?text=слон",
            "hide": True
        })

    return suggests

# Функция возвращает две расписание на текущий день недели
def get_timetable(day: str) -> dict:
    lessons = timetable[day]
    return lessons

def convert_timetable() -> str:
    day = (dt.datetime.now()).strftime('%A')
    if day in ['Saturday', 'Sunday']:
        text = 'Сегодня нет уроков радуйся дурачок'
        if 'day' == 'Saturday':
            return text
        else:
            lessons = get_timetable('Monday')
            lessons_str = '\n'.join(lessons['lessons'])
            text += f' а вот завтра есть, сейчас скажу каки:\n{lessons_str}'
    lessons = get_timetable(day)
    lessons_str = '\n'.join(lessons['lessons'])
    number_of_lessons = len(lessons['lessons'])
    text = f"Сегодня {lessons['day']}, у тебя {number_of_lessons} уроков\n{lessons_str}"
    return text

@app.route("/api", methods=['GET'])
def index() -> dict:
    day = (dt.datetime.now()).strftime('%A')
    lessons = get_timetable(day)
    return {
        'day': lessons['day'],
        'lessons': lessons['lessons']
    }
