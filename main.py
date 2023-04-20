import PySimpleGUI as sg
import lab1

def show_window():
    sg.theme('DarkBlue13')
    layout = [
        [sg.Button('Лабораторная работа №1'), sg.Button('Лабораторная работа №2'), sg.Button('Лабораторная работа №3'), sg.Button('Закрыть')]
    ]
    window = sg.Window('Программирование систем реального времени', layout)

    event, values = window.read()
    if event == 'Лабораторная работа №1':
        window.close()
        lab1.main()
    else:
        window.close()

def main():
    show_window()

# Executes main
if __name__ == '__main__':
    main()
