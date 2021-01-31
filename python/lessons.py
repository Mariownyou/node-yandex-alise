import datetime as dt

# Расписание уроков
timetable: dict = {
    'Monday': {
        'day': 'Понедельник',
        'lessons': [
            'Экономика',
            'География',
            'История',
            'Алгебра',
            'Алгебра',
            'Литература',
            'Немецкий',
            'Немецкий'
        ]
    },
    'Tuesday': {
        'day': 'Вторник',
        'lessons': [
            'Информатика',
            'Английский',
            'Русский',
            'Химия',
            'Обществознание',
            'Обществознание',
        ]
    },
    'Wednesday': {
        'day': 'Среда',
        'lessons': [
            'Фразовые глаголы',
            'Физика',
            'Литература',
            'Русский',
            'История',
            'История',
            'Словообразование'
        ]
    },
    'Thursday': {
        'day': 'Четверг',
        'lessons': [
            'Иврит',
            'Биология',
            'Английский',
            'Английский',
            'Геометрия',
            'Геометрия',
            'Русский',
            'Физкультура',
        ]
    },
    'Friday': {
        'day': 'Пятница',
        'lessons': [
            'Физика',
            'Алгебра',
            'Алгебра',
            'Английский',
            'Право',
            'Право',
            'Литература'
        ]
    },
    'Saturday': {
        'day': 'Суббота',
        'lessons': []
    },
    'Sunday': {
        'day': 'Воскреснье',
        'lessons': []
    }
}


# Функция возвращает расписание на день недели
def get_timetable(day: str) -> dict:
    lessons = timetable[day]
    return lessons


def get_current_timetable() -> dict:
    day = (dt.datetime.now()).strftime('%A')
    lessons = get_timetable(day)
    return lessons


def convert_timetable(timetable: dict, type: str = 'default') -> str:
    day = timetable['day']
    text_first = f'Сегодня {day}, '
    if type != 'default':
        text_first = f'На {day}, '
    if day in ['Суббота', 'Воскреснье']:
        text = 'Сегодня нет уроков, радуйся, дурачок'
        if day == 'Суббота':
            return text
        else:
            lessons = get_timetable('Monday')
            lessons_str = '\n'.join(lessons['lessons'])
            text += f' а вот завтра есть, сейчас скажу какие:\n{lessons_str}'
            return text
    lessons_str = '\n'.join(timetable['lessons'])
    number_of_lessons = len(timetable['lessons'])
    text = f"у тебя {number_of_lessons} уроков\n{lessons_str}"
    return text_first + text

# Парсим ответ
def parse_voice(text: str) -> str:
    parse = text.split()
    day = ''
    if 'понедельник' in parse:
        day = 'Monday'
    elif 'вторник'in parse:
        day = 'Tuesday'
    elif 'среда' in parse:
        day = 'Wednesday'
    elif 'четверг' in parse:
        day = 'Thursday'
    elif 'пятница' in parse:
        day = 'Friday'
    else:
        return 'Я глупенькая, не знаю что вам ответить. Назовите интересный вам день'
    return convert_timetable(get_timetable(day), 'n')
