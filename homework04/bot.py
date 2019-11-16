import requests
import config
import telebot
import datetime
from bs4 import BeautifulSoup


bot = telebot.TeleBot(config.schedule_bot)
telebot.apihelper.proxy = {'https': 'https://69.15.2.22:8080'}


def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule_for_a_monday(web_page):
    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу с расписанием на понедельник
    schedule_table = soup.find("table", attrs={"id": "1day"})

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list


def parse_schedule(web_page, day):
    soup = BeautifulSoup(web_page, "html5lib")

    week = ['/monday', '/tuesday', '/wednesday', '/thursday', '/friday', '/saturday', '/sunday']
    num = 0
    for week_day in range(len(week)):
        if week[week_day] == day:
            num = week_day + 1
            break

    day = '{}day'.format(num)
    # Получаем таблицу с расписанием на понедельник
    schedule_table = soup.find("table", attrs={"id": day})

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Получить расписание на указанный день """
    try:
        message_info = message.text.split()

        if len(message_info) == 2:
            day, group = message_info
            web_page = get_page(group)
        else:
            day, group, week = message_info
            web_page = get_page(group, week)

        try:
            times_lst, locations_lst, lessons_lst = parse_schedule(web_page, day)
            resp = ''
            for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
                resp += '<b>{}</b>, {}, {}\n'.format(time, location, lesson)
            bot.send_message(message.chat.id, resp, parse_mode='HTML')
        except AttributeError:
            resp = 'Занятий нет'
            bot.send_message(message.chat.id, resp, parse_mode='HTML')

    except ValueError:
        bot.send_message(message.chat.id, 'Неверная команда, попробуйте еще раз. Доступные команды: /день_недели, /all,'
                                          ' /near, /tomorrow + номер_группы', parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    n_day = datetime.datetime.weekday(datetime.datetime.today())
    n_week = datetime.date.today().isocalendar()[1]

    if n_week % 2 == 0:
        n_week = '1'
    else:
        n_week = '2'

    week = ['/monday', '/tuesday', '/wednesday', '/thursday', '/friday', '/saturday', '/sunday']
    week_day = week[n_day]

    try:
        _, group = message.text.split()

        web_page = get_page(group, n_week)

        hour = datetime.datetime.today().hour
        minutes = datetime.datetime.today().minute
        resp = ''

        times_lst, locations_lst, lessons_lst = parse_schedule(web_page, week_day)
        for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
            time = time.split('-')
            start = time[0]
            start = start.split(':')
            if len(start) < 2:
                continue
            start_h = start[0]
            start_m = start[1]
            if (int(start_h) > hour) or ((int(start_m) > minutes) and (int(start_h) == hour)):
                resp += '<b>{}</b>, {}, {}\n'.format(time, location, lesson)
                break

        while resp == '':
            try:
                n_day += 1
                if n_day == 7:
                    n_day = 0
                    if n_week == "1":
                        n_week = "2"
                    else:
                        n_week = "1"

                week_day = week[n_day]
                web_page = get_page(group, n_week)

                times_lst, locations_lst, lessons_lst = parse_schedule(web_page, week_day)
                for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
                    resp += '<b>{}</b>, {}, {}\n'.format(time, location, lesson)
                    break
            except AttributeError:
                n_day += 1
                if n_day == 7:
                    n_day = 0
                    if n_week == "1":
                        n_week = "2"
                    else:
                        n_week = "1"

    except AttributeError:
        resp = 'Неверная команда, попробуйте еще раз. Доступные команды: /день_недели, /all, ' \
               '/near, /tomorrow + номер_группы'

    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['tomorrow'])
def get_tomorrow(message):
    """ Получить расписание на следующий день """
    n_day = datetime.datetime.weekday(datetime.datetime.today()) + 1
    n_week = datetime.date.today().isocalendar()[1]
    if n_day == 7:
        n_day = 0
        n_week += 1

    if n_week % 2 == 0:
        n_week = '1'
    else:
        n_week = '2'

    try:
        week = ['/monday', '/tuesday', '/wednesday', '/thursday', '/friday', '/saturday', '/sunday']
        week_day = week[n_day]
        day, group = message.text.split()
        web_page = get_page(group, n_week)
        try:
            times_lst, locations_lst, lessons_lst = parse_schedule(web_page, week_day)
            resp = ''
            for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
                resp += '<b>{}</b>, {}, {}\n'.format(time, location, lesson)
            bot.send_message(message.chat.id, resp, parse_mode='HTML')
        except AttributeError:
            resp = 'Занятий нет'
            bot.send_message(message.chat.id, resp, parse_mode='HTML')

    except ValueError:
        bot.send_message(message.chat.id, 'Неверная команда, попробуйте еще раз. Доступные команды: /день_недели, /all,'
                                          ' /near, /tomorrow + номер_группы', parse_mode='HTML')


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    try:
        day, group = message.text.split()
        web_page = get_page(group)

        week_resp = ['<b>Понедельник:</b>\n', '<b>Вторник:</b>\n', '<b>Среда:</b>\n', '<b>Четверг:</b>\n',
                     '<b>Пятница:</b>\n', '<b>Суббота:</b>\n', '<b>Воскресенье:</b>\n']
        week = ['/monday', '/tuesday', '/wednesday', '/thursday', '/friday', '/saturday', '/sunday']
        resp = ''
        for i in range(7):
            resp_i = week_resp[i]
            try:
                times_lst, locations_lst, lessons_lst = \
                    parse_schedule(web_page, week[i])

                for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
                    resp_i += '<b>{}</b>, {}, {}\n'.format(time, location, lesson)
            except AttributeError:
                resp_i += 'Занятий нет\n'
            resp += resp_i
        bot.send_message(message.chat.id, resp, parse_mode='HTML')

    except ValueError:
        bot.send_message(message.chat.id, 'Неверная команда, попробуйте еще раз. Доступные команды: /день_недели, /all,'
                                          ' /near, /tomorrow + номер_группы', parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)
