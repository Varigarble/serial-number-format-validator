import PySimpleGUI as sg
import sam_db
import serial_formatter  # file to be renamed; put funcs in main block

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
                 [_ for _ in button_list], [sg.FileBrowse()]]
report_window = sg.Window('Report Selector', report_layout)

button_list_2 = [sg.Button(vendor) for vendor in sam_db.view_vendors()]
add_sn_layout = [[sg.Text("Pick one:")],
        [_ for _ in button_list_2]]
add_sn_window = sg.Window(layout=add_sn_layout, title="TODO: Resize Me!", element_padding=((10,10),(5,5)), size=(None, None))

pk_sn_list = [_ for _ in sam_db.view_sns()]
add_pk_layout = [[sg.Text("Pick Vendor:")],
                 [sg.Listbox(values=pk_sn_list, size=(40, 10), select_mode='multiple', key='SELECTION', enable_events=True ), \
                  sg.Button("Add", key='ADD'), sg.Multiline(default_text="selected sns go here", size=(40, 10), key='MULTILINE')]]
add_pk_window = sg.Window(layout=add_pk_layout, title="TODO: Resize Me!", element_padding=((10,10),(5,5)), size=(None, None))
#     ]  # view list of unique sns in left display box, click to move to right display box, click to remove from right display box

while True:
    event, values = primary_window.read()
    if event in ('Cancel', None):
        break
    if event == 'Add Software Vendor':
        sam_db.soft_vend_enter(sg.popup_get_text("Enter a new software vendor: "))
    if event == 'Add Serial Number':
        sn_event, sn_value = add_sn_window.read()
        add_sn_window.close()
        serial_formatter.sn_enter(sn_event, sg.popup_get_text("How many?"))
    if event == 'Add Product Key':
        while True:
            pk_event, pk_value = add_pk_window.read()
            if pk_event is None or pk_event == 'Exit':  # always check for closed window
                break
            # pending_add = [T35T]
            if pk_event == 'SELECTION':
                add_pk_window.Element('MULTILINE').Update(pk_value['SELECTION'])
                # print(pending_add)
            # if pk_event == 'ADD':
            #     add_pk_window.Element('MULTILINE').Update(pending_add)
            #     print(pending_add)
        add_pk_window.close()
        # serial_formatter.pk_in()
    if event == 'Update Software Vendor':
        pass
    if event == 'Update Serial Number':
        pass
    if event == 'Update Product Key':
        pass
    if event == 'View Vendor List':
        print(sam_db.view_vendors())
    if event == 'Get Reports':
        gr_event, gr_value = report_window.read()

primary_window.close()

# source_filename = values[0]     # the first input element is values[0]

