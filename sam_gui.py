import PySimpleGUI as sg
# import serial_formatter.py  # file to be renamed; put funcs in main block

sg.theme('Dark Blue 3')  # please make your windows colorful

primary_layout = [
    [sg.Text('Please select one of the following options:')],
    [sg.Button('Add Software Vendor'),
    sg.Button('Add Serial Number'),
    sg.Button('Add Product Key')],
    [sg.Button('Update Software Vendor'),
    sg.Button('Update Serial Number'),
    sg.Button('Update Product Key')],
    [sg.Button('View Vendor List'),
    sg.Button('Get Reports')],
    [sg.Button('Cancel')]
    ]
primary_window = sg.Window('Main Menu', primary_layout)

vend_test_list = ['Antidex', 'Abalo', 'None']  # TODO: read table names to produce current vendor list
button_list = [sg.Button(_) for _ in vend_test_list]
print(button_list)

report_layout = [[sg.Text('Which report would you like?')],
                 [_ for _ in button_list], [sg.FileBrowse()]
                 ]
report_window = sg.Window('Report Selector', report_layout)


while True:
    event, values = primary_window.read()
    if event in ('Cancel', None):
        break
    if event == 'Add Software Vendor':
        # @serial_formatter.entering_func
        serial_formatter.soft_vend_enter()
    if event == 'Add Serial Number':
        # @serial_formatter.entering_func
        serial_formatter.sn_enter()
    if event == 'Add Product Key':
        # @serial_formatter.entering_func
        serial_formatter.pk_in()
    if event == 'Update Software Vendor':
        pass
    if event == 'Update Serial Number':
        pass
    if event == 'Update Product Key':
        pass
    if event == 'Get Reports':
        gr_event, gr_value = report_window.read()

primary_window.close()

source_filename = values[0]     # the first input element is values[0]

