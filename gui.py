import PySimpleGUI as sg
from random import randint
from sacados import Population

sg.ChangeLookAndFeel('Dark')

main_layout = [
    [sg.Text('Population Size', size=(15, 1)), sg.InputText('30')],
    [sg.Text('Max weight', size=(15, 1)), sg.InputText('10')],
    [sg.Text('Max generations', size=(15, 1)), sg.InputText('1000')],
    [sg.Checkbox('Random genenration')],
    [sg.Submit()]
]

result_layout = [
    [sg.Text('Strongest child: ', text_color='red'), sg.Text('')],
    [sg.Text('Weakest child: ', text_color='red'), sg.Text('')],
    [sg.CloseButton(button_text='close')]
]

window = sg.Window('Genetic Knapsack').Layout(main_layout)
button, values = window.Read()

if values[3] == True:
    seed = randint(20, 100)
    max_weight = int(seed/2)
    n = int(0.75 * seed)
else:
    n = int(values[0])
    max_weight = int(values[1])

max_gen = int(values[2])
population = Population(max_weight, n)

population.darwin(max_generations=max_gen,gui=sg)

strong, weak = population.get_results()

sg.Popup('Results', '=======',  'Strongest child: ' + str(strong), 'Weakest child: ' + str(weak))


