import PySimpleGUI as sg
import re
import service as s
from PIL import Image
import io
import random

sg.theme('Reddit')  # Add a touch of color
# All the stuff inside your window.
text_size = (18, 1)
double_text_size = (18, 2)
input_size = (4, 1)

left_column = [
    [sg.Text('Начальные значения')],
    [sg.HorizontalSeparator()],
    [sg.Text('Объем производства', size=text_size),
     sg.Input("%.2f" % random.random(), size=input_size, key='-m1-', enable_events=True)],
    [sg.Text('Объем выбросов\nпарниковых газов', size=double_text_size),
     sg.Input("%.2f" % random.random(), size=input_size, key='-m2-', enable_events=True)],
    [sg.Text('Объем продаж', size=text_size),
     sg.Input("%.2f" % random.random(), size=input_size, key='-m3-', enable_events=True)],
    [sg.Text('Выручка', size=text_size),
     sg.Input("%.2f" % random.random(), size=input_size, key='-m4-', enable_events=True)],
    [sg.Text('Техногенные и\nэкономические риски', size=double_text_size),
     sg.Input("%.2f" % random.random(), size=input_size, key='-m5-', enable_events=True)],
    [sg.Text('Требуемые объемы\nинвестиций', size=double_text_size),
     sg.Input("%.2f" % random.random(), size=input_size, key='-m6-', enable_events=True)],
    [sg.Text('Экспорт H2', size=text_size),
     sg.Input("%.2f" % random.random(), size=input_size, key='-m7-', enable_events=True)],
    [sg.Text('ФЭС предприятий', size=text_size),
     sg.Input("%.2f" % random.random(), size=input_size, key='-m8-', enable_events=True)],
    [sg.Text('Стоимость\nпроизводства H2', size=double_text_size),
     sg.Input("%.2f" % random.random(), size=input_size, key='-m9-', enable_events=True)],
    [sg.Text('Процент водорода\nв энергобалансе', size=double_text_size),
     sg.Input("%.2f" % random.random(), size=input_size, key='-m10-', enable_events=True)],
    [sg.Text('Цифровизация, автоматизация\nи роботизация отрасли', size=(18, 3)),
     sg.Input("%.2f" % random.random(), size=input_size, key='-m11-', enable_events=True)],
    [sg.Text('Инновационная технология\nпроизводства H2', size=(18, 3)),
     sg.Input("%.2f" % random.random(), size=input_size, key='-m12-', enable_events=True)],
    # [sg.Text('Качество исходных\nматериалов и энергоресурсов', size=double_text_size),
    #  sg.Input("%.2f" % random.random(), size=input_size, key='-m13-', enable_events=True)],
    # [sg.Text('Качество образовательного\nпроцесса', size=double_text_size),
    #  sg.Input("%.2f" % random.random(), size=input_size, key='-m14-', enable_events=True)],
    # [sg.Text('Наличие и качество\nобучения кадров', size=double_text_size),
    #  sg.Input("%.2f" % random.random(), size=input_size, key='-m15-', enable_events=True)],
    # [sg.Text('Здоровье', size=text_size),
    #  sg.Input("%.2f" % random.random(), size=input_size, key='-m16-', enable_events=True)],
]

right_column = [
    [sg.Text('Уравнения')],

    [sg.Text('F', pad=(0, 0)),
     sg.Combo(values=[i for i in range(1, 121)], default_value=4, key='-f0v-'),
     sg.Text('= '),
     sg.Input("%.2f" % random.random(), size=input_size, key='-f0-d-', enable_events=True),
     sg.Text('* x^0 +', pad=(0, 0)),
     sg.Input("%.2f" % random.random(), size=input_size, key='-f0-c-', enable_events=True),
     sg.Text('* x +', pad=(0, 0)),
     sg.Input("%.2f" % random.random(), size=input_size, key='-f0-b-', enable_events=True),
     sg.Text('* x^2 +', pad=(0, 0)),
     sg.Input("%.2f" % random.random(), size=input_size, key='-f0-a-', enable_events=True),
     sg.Text('* x^3', pad=(0, 0))

     ],

    [sg.Text('F', pad=(0, 0)),
     sg.Combo(values=[i for i in range(1, 121)], default_value=10, key='-f1v-'),
     sg.Text('= '),
     sg.Input("%.2f" % random.random(), size=input_size, key='-f1-d-', enable_events=True),
     sg.Text('* x^0 +', pad=(0, 0)),
     sg.Input("%.2f" % random.random(), size=input_size, key='-f1-c-', enable_events=True),
     sg.Text('* x +', pad=(0, 0)),
     sg.Input("%.2f" % random.random(), size=input_size, key='-f1-b-', enable_events=True),
     sg.Text('* x^2 +', pad=(0, 0)),
     sg.Input("%.2f" % random.random(), size=input_size, key='-f1-a-', enable_events=True),
     sg.Text('* x^3', pad=(0, 0))
     ],

    [sg.Text('F', pad=(0, 0)),
     sg.Combo(values=[i for i in range(1, 121)], default_value=37, key='-f2v-'),
     sg.Text('= '),
     sg.Input("%.2f" % random.random(), size=input_size, key='-f2-d-', enable_events=True),
     sg.Text('* x^0 +', pad=(0, 0)),
     sg.Input("%.2f" % random.random(), size=input_size, key='-f2-c-', enable_events=True),
     sg.Text('* x +', pad=(0, 0)),
     sg.Input("%.2f" % random.random(), size=input_size, key='-f2-b-', enable_events=True),
     sg.Text('* x^2 +', pad=(0, 0)),
     sg.Input("%.2f" % random.random(), size=input_size, key='-f2-a-', enable_events=True),
     sg.Text('* x^3', pad=(0, 0))
     ],

    [sg.Text('F', pad=(0, 0)),
     sg.Combo(values=[i for i in range(1, 121)], default_value=78, key='-f3v-'),
     sg.Text('= '),
     sg.Input("%.2f" % random.random(), size=input_size, key='-f3-d-', enable_events=True),
     sg.Text('* x^0 +', pad=(0, 0)),
     sg.Input("%.2f" % random.random(), size=input_size, key='-f3-c-', enable_events=True),
     sg.Text('* x +', pad=(0, 0)),
     sg.Input("%.2f" % random.random(), size=input_size, key='-f3-b-', enable_events=True),
     sg.Text('* x^2 +', pad=(0, 0)),
     sg.Input("%.2f" % random.random(), size=input_size, key='-f3-a-', enable_events=True),
     sg.Text('* x^3', pad=(0, 0))
     ],

    [sg.Text('F', pad=(0, 0)),
     sg.Combo(values=[i for i in range(1, 121)], default_value=88, key='-f4v-'),
     sg.Text('= '),
     sg.Input("%.2f" % random.random(), size=input_size, key='-f4-d-', enable_events=True),
     sg.Text('* x^0 +', pad=(0, 0)),
     sg.Input("%.2f" % random.random(), size=input_size, key='-f4-c-', enable_events=True),
     sg.Text('* x +', pad=(0, 0)),
     sg.Input("%.2f" % random.random(), size=input_size, key='-f4-b-', enable_events=True),
     sg.Text('* x^2 +', pad=(0, 0)),
     sg.Input("%.2f" % random.random(), size=input_size, key='-f4-a-', enable_events=True),
     sg.Text('* x^3', pad=(0, 0))
     ],

    [sg.HorizontalSeparator()],
    [sg.Text('Управлние')],
    [sg.HorizontalSeparator()],
    [sg.Text('Статус', size=text_size), sg.InputText('пусто', size=(10, 1), disabled=True, key='-status-')],
    [sg.Button('Вычислить', size=text_size, key='-start-calc-')],
    [sg.Button('График', size=text_size, key='-get-func-')],
    [sg.Button('Диаграмма', size=text_size, key='-get_diag-'),
     sg.Input('0.0', size=input_size, key='-diag-time-', enable_events=True)],
    [sg.Button('Возмущения', size=text_size, key='-start-faks-')],

]

main_layout = [
    [sg.Column(left_column), sg.VerticalSeparator(), sg.Column(right_column)]
]

number_keys = ['-m' + str(i) + '-' for i in range(1, 13)]
number_keys += ['-f0-a-', '-f0-c-', '-f1-a-', '-f1-c-', '-f2-a-', '-f2-c-', '-f3-a-', '-f3-b-', '-f3-c-',
                '-f4-a-', '-f4-b-', '-f4-c-', '-diag-time-']

number_input_format = r'^[-+]?[0-9]*[.]?[0-9]{,2}$'


def check_number_fields(event, values):
    if event is not None and values is not None:
        for i in number_keys:
            if values[i] == "" and event != i:
                window[i].update(str(0.0))

            if event == i and values[i] and not re.fullmatch(number_input_format, values[i]):
                window[i].update(values[i][:-1])


# Create the Window
window = sg.Window('Водородная энергетика', main_layout, margins=(0, 0))
# Event Loop to process "events" and get the "values" of the inputs
# while True:
fak_active = False
fak_window = None

func_active = False

diag_active = False

# s.load_excel()
res = None
while True:
    event, values = window.read()
    check_number_fields(event, values)

    if event == '-start-faks-':
        fak_active = True

    if event == '-start-calc-':
        s.chars.init_par(values)

        try:
            res = s.chars.calculate(values)
            window['-status-'].update('готово')
        except BaseException:
            window['-status-'].update('нет решений')

    if event == '-get-func-':
        if res is not None:
            func_active = True

    if event == '-get_diag-':
        if res is not None:
            diag_active = True

    if diag_active:
        s.chars.get_diag(float(values['-diag-time-']))
        image = Image.open('diag.png')
        # image.thumbnail((400, 400))
        bio = io.BytesIO()
        image.save(bio, format="PNG")
        diag_layout = [
            [sg.Image(key='-Diag-', data=bio.getvalue())],
            [sg.Button('Закрыть', key='Exit')],
        ]
        win_diag = sg.Window("Диаграмма", diag_layout)
        while True:
            event_diag, values_diag = win_diag.read()
            if event_diag in (sg.WIN_CLOSED, 'Exit'):
                diag_active = False
                win_diag.close()
                break

    if func_active:
        s.chars.get_graphics()
        image = Image.open('funcs.png')
        # image.thumbnail((400, 400))
        bio = io.BytesIO()
        image.save(bio, format="PNG")
        funcs_layout = [
            [sg.Image(key='-Funcs-', data=bio.getvalue())],
            [sg.Button('Закрыть', key='Exit')],
        ]
        win_funcs = sg.Window("График", funcs_layout)
        while True:
            event_funcs, values_funcs = win_funcs.read()
            if event_funcs in (sg.WIN_CLOSED, 'Exit'):
                func_active = False
                win_funcs.close()
                break

    if fak_active:
        s.get_faks_image()
        image = Image.open('fak.png')
        # image.thumbnail((400, 400))
        bio = io.BytesIO()
        image.save(bio, format="PNG")
        fak_layout = [
            [sg.Image(key='-Faks-', data=bio.getvalue())],
            [sg.Button('Закрыть', key='Exit')],
        ]
        win_fak = sg.Window("Возмущения", fak_layout)
        while True:
            event_fak, values_fak = win_fak.read()
            if event_fak in (sg.WIN_CLOSED, 'Exit'):
                fak_active = False
                win_fak.close()
                break

    if event in (sg.WIN_CLOSED, 'Exit'):
        break

window.close()
