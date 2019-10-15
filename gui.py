import PySimpleGUI as sg

sg.ChangeLookAndFeel('Dark')

main_layout = [
    [sg.Text('Population Size', size=(15, 1)), sg.InputText('')],
    [sg.Text('Max weight', size=(15, 1)), sg.InputText('')],
    [sg.Submit()]
]

result_layout = [
    [sg.Text('Strongest child: ', text_color='red'), sg.Text('')],
    [sg.Text('Weakest child: ', text_color='red'), sg.Text('')],
    [sg.CloseButton(button_text='close')]
]

window = sg.Window('Genetic Knapsack').Layout(main_layout)
button, values = window.Read()
