from datetime import datetime
import console_ui as ui
from dataIO import load_from_json, save_to_json


def add_new():
    title = ui.get_string('Введите заголовок заметки: ')
    if not title:
        ui.show_string('Заголовок не может быть пустым.')
        return
    body = ui.get_string('Введите тело заметки: ')
    if not body:
        ui.show_string('Тело заметки не может быть пустым.')
        return
    id = 0
    if len(data) != 0:
        id = data[len(data) - 1]['id'] + 1
    data.append({'id': id, 'title': title, 'body': body, 'date': datetime.now()})


def show_help():
    ui.show_string(command_list)


def save():
    save_to_json(path, data)


def get_index(id_or_title):
    try:
        id_or_bust = int(id_or_title)
        for i in range(len(data)):
            if data[i]['id'] == id_or_bust:
                return i
    except ValueError:
        matches = list()
        for i in range(len(data)):
            if data[i]['title'] == id_or_title:
                matches.append(i)
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            return matches
    return -1


def note_to_str(note: dict):
    if list(note.keys()) == ['id', 'title', 'body', 'date']:
        return f'id: {note["id"]}; заголовок: {note["title"]}; ' \
               f'тело заметки: {note["body"]}; дата последнего изменения: {note["date"].strftime("%H:%M %d/%m/%Y")}'
    raise ValueError('Not a valid note.')


def choose_from(indexes: list):
    ui.show_string('Было найдено несколько совпадений, '
                   'укажите какую заметку вы имели ввиду, введите "all", чтобы выбрать все: ')
    for i in range(len(indexes)):
        ui.show_string(f'{i} - {note_to_str(data[indexes[i]])}')
    choice = ui.get_string('Ваш выбор: ')
    if choice == 'all':
        return 'all'
    try:
        index = int(choice)
        if 0 <= index < len(indexes):
            return indexes[index]
    except ValueError:
        pass
    ui.show_string(f'Некорректный выбор {choice}.')
    return 'fail'


def show(title_or_id: str):
    if title_or_id == 'all':
        for i in range(len(data)):
            show(str(i))
        return
    index = get_index(title_or_id)
    if type(index) is list:
        for i in index:
            show(i)
        return
    if index == -1:
        ui.show_string(f'Не найдена заметка с индексом или заголовком {title_or_id}.')
        return
    ui.show_string(note_to_str(data[index]))


def edit_inner(index: int):
    new_title = ui.get_string('Введите новый заголовок, не вводите ничего, чтобы не менять: ')
    new_body = ui.get_string('Введите новое тело заметки, не вводите ничего, чтобы не менять: ')
    changed = False
    if new_title:
        data[index]['title'] = new_title
        changed = True
    if new_body:
        data[index]['body'] = new_body
        changed = True
    if changed:
        data[index]['date'] = datetime.now()


def edit(title_or_id: str):
    index = get_index(title_or_id)
    if type(index) is list:
        choice = choose_from(index)
        if choice == 'fail':
            return
        if choice == 'all':
            for i in index:
                edit(str(i))
        else:
            edit(str(choice))
        return
    if index == -1:
        ui.show_string(f'Не найдена заметка с индексом или заголовком {title_or_id}.')
        return
    edit_inner(index)


def delete(title_or_id: str):
    if title_or_id == 'all':
        for i in range(len(data)):
            delete(str(i))
        return
    index = get_index(title_or_id)
    if type(index) is list:
        choice = choose_from(index)
        if choice == 'fail':
            return
        if choice == 'all':
            for i in index:
                delete(str(i))
        else:
            delete(str(choice))
        return
    if index == -1:
        ui.show_string(f'Не найдена заметка с индексом или заголовком {title_or_id}.')
        return
    del data[index]


def execute_command(command: str):
    match command:
        case 'help': show_help()
        case 'new': add_new()
        case 'save': save()
        case 'exit': return False
        case _:
            if command.startswith('show '):
                show(command.removeprefix('show '))
            elif command.startswith('edit '):
                edit(command.removeprefix('edit '))
            elif command.startswith('delete '):
                delete(command.removeprefix('delete '))
            else:
                ui.show_string(f'Команда {command} не найдена. Попробуйте снова.')
    return True


def main():
    init()
    cycle = True
    while cycle:
        cycle = execute_command(ui.get_string('Введите команду: '))


def init():
    global path
    path = ui.get_string('Введите путь к файлу, с которым хотите работать или "default", '
                         'чтобы работать с файлом по умолчанию (notes.json): ')
    path = default_path if path.lower() == 'default' else path
    global data
    data = load_from_json(path)
    if type(data) is str:
        ui.show_string(data)
        ui.show_string('Работа продолжается с пустым списком.')
        data = list()
    ui.show_string(command_list)


if __name__ == '__main__':
    default_path = 'notes.json'
    command_list = 'Список команд:\n' \
                   'help - Вывод списка команд.\n' \
                   'new - Запуск процесса добавления новой заметки.\n' \
                   'save - Сохранение в файл всех изменений с момента последнего сохранения.\n' \
                   'show <id/title/all> - Вывод заметки по индексу или заголовку или всех заметок.\n' \
                   'edit <id/title> - Запуск процесса изменения заметки по индексу или заголовку.\n' \
                   'delete <id/title/all> - Удаление заметки по индексу или заголовку или всех заметок.\n' \
                   'exit - Завершение работы программы.'
    data: list
    path: str
    main()
