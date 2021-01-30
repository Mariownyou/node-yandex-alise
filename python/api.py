# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging

# Импортируем datetime и timetable
import datetime as dt
from lessons import 
    timetable, 
    get_current_timetable, 
    get_timetable, 
    convert_timetable, 
    parse_voice,

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
                "Понедельник",
                "Вторник",
                "Среда",
                "Четверг",
                "Пятница"
            ]
        }

        res['response']['text'] = convert_timetable(get_current_timetable())
        res['response']['buttons'] = get_suggests(user_id, sessionStorage)
        return

    # Обрабатываем ответ пользователя.
    res['response']['text'] = parse_voice(req['request']['original_utterance'].lower())
    res['response']['buttons'] = get_suggests(user_id, sessionStorage)
    return

# Функция возвращает две подсказки для ответа.
def get_suggests(user_id) -> dict:
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests']
    ]

    return suggests

@app.route("/api", methods=['GET'])
def index() -> dict:
    day = (dt.datetime.now()).strftime('%A')
    lessons = get_timetable(day)
    return {
        'day': lessons['day'],
        'lessons': lessons['lessons']
    }

@app.route("/api/<day>", methods=['GET'])
def lessons(day: str) -> str:
    timetable = get_timetable(day)
    text = convert_timetable(timetable)
    return text
