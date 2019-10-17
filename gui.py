import PySimpleGUI as sg
from random import randint
from knapsack import Population

sg.ChangeLookAndFeel('Dark')

main_layout = [
    [sg.Text('Population Size', size=(15, 1)), sg.InputText('30')],
    [sg.Text('Max weight', size=(15, 1)), sg.InputText('10')],
    [sg.Text('Max generations', size=(15, 1)), sg.InputText('1000')],
    [sg.Checkbox('Random genenration')],
    [sg.Submit()]
]


main_window = sg.Window('Genetic Knapsack').Layout(main_layout)
button, values = main_window.Read()

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

result_layout = [
    [sg.Text('Results', justification='center', font='Helvetica 20', auto_size_text=True)],
    [sg.Text('Number of generations: '), sg.Text(str(population.current_gen+1))],
    [sg.Text('Strongest child: ', text_color='green'), sg.Text(str(strong))],
    [sg.Text('Weakest child: ', text_color='red'), sg.Text(str(weak))],
    [sg.CloseButton(button_text='Close')]
]

result_window = sg.Window('Results').Layout(result_layout)

button, values = result_window.Read()





  






   
       



        