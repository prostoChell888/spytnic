import PySimpleGUI as sg

import calculator

import math
import DateTime
import Efermids
import efermidParameters
import Satellite


def string_to_numbers(string):
    numbers = []
    string = string.replace("D", "E")
    i = j = 0
    while i < len(string):
        if (string[i] == " ") or (string[i] == "*"):
            i += 1
            continue
        j = i + 1
        while j < len(string):
            if (string[j] == " ") or (
                    string[j] == "-" and string[j - 1] in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")):
                break
            j += 1
        str_num = string[i:j]
        numbers.append(float(str_num))
        i = j
    return numbers


def read_orbits(strList):
    res = []
    for i in range(0, len(strList) - 1, 8):
        tmp = Satellite.Satellite()
        numbers = string_to_numbers(strList[i])
        tmp.numberS = int(numbers[0])
        tmp.TOC = DateTime.DateTime(int(numbers[1]) + 2000, int(numbers[2]), int(numbers[3]), int(numbers[4]),
                                    int(numbers[5]), int(numbers[6]))
        numbers = string_to_numbers(strList[i + 1])
        tmp.deltaN = numbers[2]
        tmp.M0 = numbers[3]
        tmp.CRS = numbers[1]
        numbers = string_to_numbers(strList[i + 2])
        tmp.CUC = numbers[0]
        tmp.e0 = numbers[1]
        tmp.CUS = numbers[2]
        tmp.sqrtA = numbers[3]
        numbers = string_to_numbers(strList[i + 3])
        tmp.tOE = int(numbers[0])
        tmp.CIC = numbers[1]
        tmp.omega0 = numbers[2]
        tmp.CIS = numbers[3]
        numbers = string_to_numbers(strList[i + 4])
        tmp.I0 = numbers[0]
        tmp.CRC = numbers[1]
        tmp.w = numbers[2]
        tmp.OMEGADOT = numbers[3]
        numbers = string_to_numbers(strList[i + 5])
        tmp.IDOT = numbers[0]
        res.append(tmp)
    return res


def parseEfermid(efermids):
    res = []
    i = 0
    while i < len(efermids) - 2:
        ef = Efermids.Efermids()
        numbers = string_to_numbers(efermids[i][3:len(efermids[i]) - 3])
        int_numbers = []
        for temp_i in range(len(numbers)):
            int_numbers.append(int(numbers[temp_i]))
        ef.set_datatime(
            DateTime.DateTime(int_numbers[0], int_numbers[1], int_numbers[2], int_numbers[3], int_numbers[4],
                              int_numbers[5]))
        i += 1
        tmp = []
        while i < len(efermids) - 2 and efermids[i][0] != '*':
            parameters_string = efermids[i][5:len(efermids[i]) - 5]
            j = 0
            while j < len(parameters_string) and parameters_string[j] == ' ':
                j += 1
            numbers = string_to_numbers(parameters_string[j:len(parameters_string) - j])
            ef_parameters = efermidParameters.efirmidParametrs()
            ef_parameters.nameS = efermids[i][0:4]
            ef_parameters.set_x(numbers[0])
            ef_parameters.set_y(numbers[1])
            ef_parameters.set_z(numbers[2])
            tmp.append(ef_parameters)
            i += 1
        ef.set_parameters(tmp)
        res.append(ef)
    return res


headings = ['Satellite №', 'Date', 'Time', 'delta_x', 'delta_y', 'delta_z']


# готово
def popup_get_2files(message, title=None):
    layout = [
        [sg.Text('GPS Navigation File: ')],
        [sg.Input(key='-INPUT1-'),
         sg.FilesBrowse('Найти', file_types=((("All Files", "*"),)))],
        [sg.Text('Ультрабыстрые эфиримиды: ')],
        [sg.Input(key='-INPUT2-'),
         sg.FilesBrowse('Найти', file_types=((("All Files", "*"),)))],
        [sg.Button('Ok'), sg.Button('Отмена')],
    ]
    window = sg.Window(title if title else message, layout)
    event, values = window.read(close=True)
    return [values['-INPUT1-'], values['-INPUT2-']] if event == 'Ok' else None


def read_23n(filename):
    if filename == '':
        return
    file = open(filename, "r")
    header_rows = tmp = 0
    data = []
    for row in file:
        if header_rows == 0:
            if row.split()[0] != "END":
                tmp += 1
            else:
                header_rows = tmp + 1
            continue
        data.append(row)
    file.close()
    return data


def read_sp3(filename):
    if filename == '':
        return
    file = open(filename, "r")
    header_rows = -1
    tmp = 0
    efirmids_rows = []
    for row in file:
        if header_rows == -1:
            if row.split()[0] != "*":
                tmp += 1
                continue
            else:
                header_rows = tmp
        efirmids_rows.append(row)
    file.close()
    return efirmids_rows


def remove_none_rows(data, xI, yI):
    new_data = []
    for row in data:
        if row[xI] and row[yI]:
            new_data.append(row)
    return new_data


def show_window(data):
    menu_def = [
        ['Файл', ['Новый файл', 'Открыть JSON', 'Открыть файл', 'Открыть файлы', '---', 'Сохранить в JSON', 'Закрыть']],
        ['Инструменты', ['Таблицы', 'График', 'Стат. данные']],
        ['Настройки', ['Единицы измерения', 'Другое']]]

    table = [
        [sg.Text('Рассчитанные значения: ')],
        [sg.Table(values=data,
                  key='table',
                  headings=headings,
                  font='Helvetica',
                  pad=(25, 25),
                  display_row_numbers=False,
                  auto_size_columns=True,
                  vertical_scroll_only=False,
                  # def_col_width=5,
                  # max_col_width=5,
                  num_rows=min(20, len(data)))]
    ]

    layout = [[sg.Menu(menu_def, background_color='lightsteelblue', text_color='navy', disabled_text_color='yellow',
                       font='Verdana', pad=(10, 10))],
              [table],
              [sg.Text('_' * 150)],
              [sg.Button('Закрыть')]
              ]
    window = sg.Window('Лабораторная работа 1', layout)
    while True:  # The Event Loop
        event, values = window.read()
        print(event)
        print(values)
        if event in (None, 'Exit', 'Закрыть'):
            window.close()
            break


def main():
    sg.set_options(auto_size_buttons=True)
    filenames = popup_get_2files("Выберите файлы...")
    satellites_data = read_23n(filenames[0])
    efirmids_rows = read_sp3(filenames[1])
    res = read_orbits(satellites_data)
    numbers = set()
    for satellite in res:
        numbers.add(satellite.numberS)
    efirmids = parseEfermid(efirmids_rows)

    table_values = []
    for num in numbers:
        for i in range(0, len(res)):
            if res[i].numberS == num:
                coords = calculator.calculateSpeeds(res[i])
                j = 0
                while j < len(efirmids) and not efirmids[j].get_datatime().is_equal(res[i].TOC):
                    j += 1
                if j < len(efirmids):
                    satellite_name = "PG"
                    if res[i].numberS < 10:
                        satellite_name += "0"
                    satellite_name = satellite_name + str(res[i].numberS)

                    k = 0
                    while k < len(efirmids[j].get_parameters()) and efirmids[j].get_parameters()[k].nameS != satellite_name:
                        k += 1
                    if (k >= len(efirmids[j].get_parameters())):
                        k = len(efirmids[j].get_parameters()) - 1
                    deltaX = abs(abs(coords[0]) - abs(efirmids[j].get_parameters()[k].get_x()))
                    deltaY = abs(abs(coords[1]) - abs(efirmids[j].get_parameters()[k].get_y()))
                    deltaZ = abs(abs(coords[2]) - abs(efirmids[j].get_parameters()[k].get_z()))
                    print("    {}   |{}|{}|{:.17f}|{:.17f}|{:.17f}".format(satellite_name, res[i].TOC.date_to_string(), res[i].TOC.time_to_string().ljust(6), deltaX, deltaY, deltaZ))
        print("\nSatellite №|   date  | time","|   delta X (Km.)".ljust(19), "|   delta Y (Km.)".ljust(19), "|   delta Z (Km.)".ljust(19))
        print("-----------------------------------------------------------------------------------------")

    show_window(table_values)
    print(table_values)
    # Executes main


if __name__ == '__main__':
    main()

