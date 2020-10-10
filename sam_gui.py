import PySimpleGUI as sg
import sam_db
import serial_formatter  # file to be renamed; put funcs in main block

sg.theme('Dark Blue 3')  # please make your windows colorful

def main():
    # Main menu
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


    # Reports window
    button_list = [sg.Button(vendor) for vendor in sam_db.view_vendors()]
    report_layout = [[sg.Text('Which report would you like?')],
                     [_ for _ in button_list], [sg.FileBrowse()]]
    report_window = sg.Window('Report Selector', report_layout)

    # Vendor Query window
    button_list = [sg.Button(vendor) for vendor in sam_db.view_vendors()]
    vendor_query_layout = [[sg.Listbox(values=sam_db.view_vendors(), size=(64, 32))]]
    vendor_query_window = sg.Window(layout=vendor_query_layout, title="Here are all the vendors")


    pk_sn_list = [_ for _ in sam_db.view_sns()]

    while True:
        # Main menu
        event, values = primary_window.read()

        if event in ('Cancel', None):
            print("Exiting Program")
            exit()

        # Add Software Vendor
        if event == 'Add Software Vendor':
            while True:
                sv_event = sg.popup_get_text("Enter a new software vendor: ")
                if sv_event in ('Cancel', None):
                    break
                else:
                    sam_db.soft_vend_enter((sv_event))


        # Add Serial Number
        if event == 'Add Serial Number':
            button_list = [sg.Button(vendor) for vendor in sam_db.view_vendors()]
            add_sn_layout = [[sg.Text("Pick one:")],
                             [_ for _ in button_list]]
            add_sn_window = sg.Window(layout=add_sn_layout, title="TODO: Resize Me!",
                                      element_padding=((10, 10), (5, 5)), size=(None, None))
            while True:
                sn_event, sn_value = add_sn_window.read()
                if sn_event in ('Cancel', None):  # always check for closed window
                    add_sn_window.close()
                    break
                else:
                    serial_formatter.sn_enter(sn_event, sg.popup_get_text("How many?"))

        # Add Product Key
        if event == 'Add Product Key':
            add_pk_layout = [[sg.Text("Pick Vendor:")],
                             [sg.Listbox(values=pk_sn_list, size=(40, 10), select_mode='multiple', key='SELECTION',
                                         enable_events=True), \
                              sg.Multiline(default_text="selected sns go here", size=(40, 10), key='MULTILINE'),
                              sg.Button("Go")]]
            add_pk_window = sg.Window(layout=add_pk_layout, title="TODO: Resize Me!",
                                      element_padding=((10, 10), (5, 5)), size=(None, None))
            """view list of unique sns in left display box, click to move to right display box, click to remove from 
            right display box"""
            while True:
                pk_event, pk_value = add_pk_window.read()
                if pk_event is None or pk_event == 'Exit':  # always check for closed window
                    add_pk_window.close()
                    break
                if pk_event == 'SELECTION':
                    add_pk_window.Element('MULTILINE').Update(pk_value['SELECTION'])
                if pk_event == 'Go':
                    pass
                # serial_formatter.pk_in()

        if event == 'Update Software Vendor':
            pass
        if event == 'Update Serial Number':
            pass
        if event == 'Update Product Key':
            pass

        # Vendor query
        if event == 'View Vendor List':
            print(sam_db.view_vendors())
            while True:
                vq_event, vq_value = vendor_query_window.read()
                if vq_event == sg.WIN_CLOSED or vq_event == 'Exit':
                    vendor_query_window.close()
                    break


        # Reports
        if event == 'Get Reports':
            gr_event, gr_value = report_window.read()

    primary_window.close()

main()

