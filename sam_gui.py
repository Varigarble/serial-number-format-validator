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


    while True:
        # Main menu
        event, values = primary_window.read()

        if event in ('Cancel', None):
            print("Exiting Program")
            exit()

        if event == 'Add Software Vendor':
            while True:
                sv_event = (sg.popup_get_text("Enter a new software vendor: "))
                if sv_event in ('Cancel', None):
                    break
                elif sv_event.lower() in [v.lower() for v in sam_db.view_vendors()]:
                    add_sv_layout = [[sg.Text("That vendor already exists. Do you want to add more licenses for it?")],
                                     [sg.Button('Yes'), sg.Button('No')]]
                    add_sv_window = sg.Window(layout=add_sv_layout, title="Confirm Vendor Addition")
                    while True:
                        add_sv_event, add_sv_value = add_sv_window.read()
                        if add_sv_event in ('Cancel', None, 'No'):
                            add_sv_window.close()
                            break
                        if add_sv_event == 'Yes':
                            # TODO: add option for multiple entries
                            sam_db.soft_vend_enter(sv_event)
                else:
                    sam_db.soft_vend_enter(sv_event)

        if event == 'Add Serial Number':
            button_list = [sg.Button(vendor) for vendor in sam_db.view_vendors()]
            add_sn_layout = [[sg.Text("Pick one:")],
                             [_ for _ in button_list]]
            add_sn_window = sg.Window(layout=add_sn_layout, title="Add Serial Number",
                                      element_padding=((10, 10), (5, 5)), size=(None, None))
            while True:
                sn_event, sn_value = add_sn_window.read()
                if sn_event in ('Cancel', None):  # always check for closed window
                    add_sn_window.close()
                    break
                else:
                    try:
                        sn_amount = (sg.popup_get_text("How many?"))
                        if sn_amount is None or sn_amount == 'Exit':
                            event = 'Add Serial Number'
                        if sn_amount:
                            if not sn_amount.isdigit():
                                raise TypeError(sg.popup("Please enter an integer"))
                    except TypeError:
                        event = 'Add Serial Number'
                    else:
                        if sn_amount:
                            sn_add_list = [_ for _ in serial_formatter.sn_enter(sn_event, sn_amount)]
                            sn_confirm_layout = [
                                [sg.Text(f"ARE YOU SURE YOU WANT TO ADD {sn_amount} LICENSE(S) OF {sn_event} WITH SERIAL NUMBER {sn_add_list[0][1]}?")],
                                [sg.Button('Yes'), sg.Button('No')]
                                ]
                            sn_confirm_window = sg.Window(layout=sn_confirm_layout, title="CAUTION")
                            while True:
                                sn_confirm_event, sn_confirm_values = sn_confirm_window.read()
                                if sn_confirm_event == 'Yes':
                                    sam_db.sn_write(sn_add_list)
                                    sn_confirm_window.close()
                                elif sn_confirm_event == 'No':
                                    sn_confirm_window.close()
                                    break
                                else:
                                    if sn_confirm_event in ('Cancel', None):
                                        break

        if event == 'Add Product Key':
            pk_list = sam_db.view_all_avail_pk_namedtuple()
            pk_set_out = set()
            add_pk_layout = [[sg.Text("Pick Vendor:")],
                             [sg.Listbox(values=pk_list, size=(40, 10), select_mode='multiple', key='SELECTION',
                                         enable_events=True),
                              sg.Listbox(values=["selected sns go here"], size=(40, 10), key='UPDATE'),
                              sg.Button('Go')]]
            add_pk_window = sg.Window(layout=add_pk_layout, title="Add Product Key",
                                      element_padding=((10, 10), (5, 5)), size=(None, None))
            """view list of unique sns in left display box, click to move to right display box, click to remove from 
            right display box"""
            while True:
                pk_event, pk_value = add_pk_window.read()
                if pk_event is None or pk_event == 'Exit':  # always check for closed window
                    add_pk_window.close()
                    break
                if pk_event == 'SELECTION':
                    add_pk_window.Element('UPDATE').Update(pk_value['SELECTION'])
                if pk_event == 'Go':  # TODO: send selected to serial_formatter.pk_enter()
                    initial_key = sg.popup_get_text('Enter Product Key: ')
                    for row in pk_value['SELECTION']:
                        row_pk_mod = row._replace(Product_Key=initial_key)
                        pk_set_out.add(row_pk_mod)
                    print("pk_set_out:", pk_set_out)


        if event == 'Update Software Vendor':
            button_list = [sg.Button(vendor) for vendor in sam_db.view_vendors()]
            usv_layout = [[sg.Text("Select a vendor to modify")], [_ for _ in button_list]]
            usv_window = sg.Window(layout=usv_layout, title="Update Software Vendor")
            while True:
                usv_event, usv_values = usv_window.read()
                if usv_event is None or usv_event == 'Exit':
                    usv_window.close()
                    break
                else:  # TODO: SQL change vendors in sam_db.py
                    usv_vendor = sg.popup_get_text(f"Enter the corrected name of: {usv_event}")
                    if usv_vendor is None or usv_vendor == 'Exit':
                        event = 'Update Software Vendor'
                    else:
                        usv_confirm_layout = [[sg.Text(f"ARE YOU SURE YOU WANT TO CHANGE {usv_event} to {usv_vendor}?")],
                                               [sg.Button('Yes'), sg.Button('No')]
                                              ]
                        usv_confirm_window = sg.Window(layout=usv_confirm_layout, title="CAUTION")
                        while True:
                            usvc_event, usvc_values = usv_confirm_window.read()
                            if usvc_event == 'Yes':
                                print(usv_vendor)
                                usv_confirm_window.close()
                            elif usvc_event == 'No':
                                usv_confirm_window.close()
                                break
                            else:
                                if usvc_event in ('Cancel', None):
                                    break

        if event == 'Update Serial Number':
            update_sn_list = [_ for _ in sam_db.view_all()]
            update_sn_layout = [[sg.Text("Select Vendor/Serial Number:")],
                             [sg.Listbox(values=update_sn_list, size=(40, 10), key='SN_SELECTION',
                                         enable_events=True),
                              sg.Button('Go')]]
            update_sn_window = sg.Window(layout=update_sn_layout, title="Update Serial Number")
            while True:
                up_sn_event, up_sn_value = update_sn_window.read()
                if up_sn_event is None or up_sn_event == 'Exit':
                    update_sn_window.close()
                    break
                if up_sn_event == 'Go':  # TODO: SQL change s/ns in serial_formatter.py
                    print(up_sn_value['SN_SELECTION'])

        if event == 'Update Product Key':
            update_pk_list = [_ for _ in sam_db.view_all()]
            update_pk_layout = [[sg.Text("Select Vendor/Serial Number:")],
                                [sg.Listbox(values=update_pk_list, size=(40, 10), key='PK_SELECTION',
                                            enable_events=True, select_mode='multiple'),
                                 sg.Button('Go')]]
            update_pk_window = sg.Window(layout=update_pk_layout, title='Update Product Key')
            while True:
                up_pk_event, up_pk_value = update_pk_window.read()
                if up_pk_event is None or up_pk_event =='Exit':
                    update_pk_window.close()
                    break
                if up_pk_event == 'Go':  # TODO: SQL change product keys in serial_formatter.py
                    print(up_pk_value['PK_SELECTION'])

        if event == 'View Vendor List':
            # button_list = [sg.Button(vendor) for vendor in sam_db.view_vendors()]
            vendor_query_layout = [[sg.Listbox(values=sam_db.view_vendors(), size=(64, 32))]]
            vendor_query_window = sg.Window(layout=vendor_query_layout, title="Here are all the vendors")
            print(sam_db.view_vendors())
            while True:
                vq_event, vq_value = vendor_query_window.read()
                if vq_event is None or vq_event == 'Exit':
                    vendor_query_window.close()
                    break

        if event == 'Get Reports':
            button_list = [sg.Button(vendor) for vendor in sam_db.view_vendors()]
            report_layout = [[sg.Text("Which report would you like?")],
                             [_ for _ in button_list], [sg.FileBrowse()]]
            report_window = sg.Window('Report Selector', report_layout)
            while True:
                gr_event, gr_value = report_window.read()
                if gr_event is None or gr_event == 'Exit':
                    report_window.close()
                    break


main()

