import PySimpleGUI as sg

sg.theme('Dark Blue 3')  # please make your windows colorful

layout = [[sg.Text('Which report would you like?')],
                 [sg.Button(button_text='Antidex'), sg.FileBrowse()],
                 ]

window = sg.Window('Simple Report Selector', layout)

event, values = window.read()
window.close()

source_filename = values[0]     # the first input element is values[0]

