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
                            add_sv_window.close()
                            continue
                try:
                    vendor_amount = (sg.popup_get_text("How many licenses do you want to add?"))
                    if vendor_amount is None or vendor_amount == 'Exit':
                        break
                    if vendor_amount:
                        if not vendor_amount.isdigit():
                            raise TypeError(sg.popup("Please enter an integer"))
                except TypeError:
                    event = 'Add Software Vendor'
                else:
                    if vendor_amount:
                        sam_db.soft_vend_enter(sv_event, int(vendor_amount))
                        break

        if event == 'Add Serial Number':
            # adds serial numbers (sn) to entries that have none
            sn_list = sam_db.view_all_none_sn_namedtuple()
            # the sn_list index is hardcoded to the items so that we can see the exact items that wil be updated:
            enumerated_sn_list = list(enumerate(sn_list))
            # make a subset of data for a pretty display:
            gui_sn_list = [f"Vendor: {row.Vendor}, Product Key: {row.Product_Key}" for row in sn_list]
            sn_set_out = set()
            add_sn_layout = [[sg.T("Pick Vendor(s):")],
                            [sg.Listbox(values=gui_sn_list, size=(100, 10), select_mode='multiple', key='SELECTION',
                                        enable_events=True, metadata=())],
                            [sg.Listbox(values=["Selected rows go here"], size=(100, 10), key='UPDATE')],
                            [sg.B("View Metada", key='-META-'), sg.B("Go")]]
            add_sn_window = sg.Window(layout=add_sn_layout, title="Add Serial Number",
                                      element_padding=((10, 10), (5, 5)), size=(None, None))
            while True:
                sn_event, sn_value = add_sn_window.read()
                if sn_event is None or sn_event == 'Exit':
                    add_sn_window.close()
                    break
                if sn_event == 'SELECTION':  # add/remove selected to right/lower box
                    # replace existing metadata with a tuple of the indexes of highlighted items in the Listbox:
                    add_sn_window.Element('SELECTION').metadata = add_sn_window.Element('SELECTION').GetIndexes()
                    # copy the pretty display of items into a second Listbox:
                    add_sn_window.Element('UPDATE').Update(sn_value['SELECTION'])
                if sn_event == "-META-":  # for testing purposes
                    print("metadata: ", add_sn_window.Element('SELECTION').metadata)
                if sn_event == 'Go':
                    initial_key = sg.popup_get_text("Enter Serial Number: ")
                    for row in enumerated_sn_list:
                        # compare complete namedtuple rows to index values of selected gui rows:
                        if enumerated_sn_list.index(row) in add_sn_window.Element('SELECTION').metadata:
                            # send row to validate serial against regex, request new serial number until validated
                            if serial_formatter.sn_checker(row, initial_key) != row:
                                try_key = sg.popup_get_text(str(f"{initial_key} is not a valid serial number for "
                                                                f"{row[1].Vendor}, Product Key: {row[1].Product_Key}"))
                                while serial_formatter.sn_checker(row, try_key) != row and try_key is not None:
                                    try_key = sg.popup_get_text(str(f"{try_key} is not a valid serial number for "
                                                                    f"{row[1].Vendor}, Product Key: {row[1].Product_Key}"))
                                row_sn_mod = row[1]._replace(Serial_Number=try_key)  # enumeration discarded
                                sn_set_out.add(row_sn_mod)
                            else:
                                row_sn_mod = row[1]._replace(Serial_Number=initial_key)  # enumeration discarded
                                sn_set_out.add(row_sn_mod)
                    add_sn_window.Element('UPDATE').Update(["Updated Items:"] + [f"Vendor: {row.Vendor}, Serial Number: "
                                                            f"{row.Serial_Number}, Product Key: {row.Product_Key}" for
                                                            row in sn_set_out])
                    print("sn_set_out post-mod:", sn_set_out)  # for testing purposes
                    sam_db.serial_one_row_updater(sn_set_out)
                    sn_set_out = set()  # empty the set for re-use

        if event == 'Add Product Key':
            # adds product keys (pk) to entries that have none
            pk_list = sam_db.view_all_none_pk_namedtuple()  # original list
            # the pk_list index is hardcoded to the items so that we can see the exact items that wil be updated:
            enumerated_pk_list = list(enumerate(pk_list))
            # make a subset of data for a pretty display:
            gui_pk_list = [f"Vendor: {row.Vendor}, Serial Number: {row.Serial_Number}" for row in pk_list]
            pk_set_out = set()  # collect rows with new pks in here
            add_pk_layout = [[sg.Text("Pick Vendor(s):")],
                             [sg.Listbox(values=gui_pk_list, size=(100, 10), select_mode='multiple', key='SELECTION',
                                         enable_events=True, metadata=())],
                              [sg.Listbox(values=["Selected rows go here"], size=(100, 10), key='UPDATE')],
                              [sg.B("View Metadata", key='-META-'), sg.Button("Go")]]
            add_pk_window = sg.Window(layout=add_pk_layout, title="Add Product Key",
                                      element_padding=((10, 10), (5, 5)), size=(None, None))
            while True:
                pk_event, pk_value = add_pk_window.read()
                if pk_event is None or pk_event == 'Exit':  # always check for closed window
                    add_pk_window.close()
                    break
                if pk_event == 'SELECTION':  # add/remove selected to right/lower box
                    # replace existing metadata with a tuple of the indexes of highlighted items in the Listbox:
                    add_pk_window.Element('SELECTION').metadata = add_pk_window.Element('SELECTION').GetIndexes()
                    # copy the pretty display of items into a second Listbox:
                    add_pk_window.Element('UPDATE').Update(pk_value['SELECTION'])
                if pk_event == "-META-":  # for testing purposes
                    print("metadata: ", add_pk_window.Element('SELECTION').metadata)
                if pk_event == 'Go':
                    initial_key = sg.popup_get_text("Enter Product Key: ")
                    for row in enumerated_pk_list:
                        # compare complete namedtuple rows to index values of selected gui rows:
                        if enumerated_pk_list.index(row) in add_pk_window.Element('SELECTION').metadata:
                            # send row to validate product key against regex, request new product key until validated
                            if serial_formatter.pk_checker(row, initial_key) != row:
                                try_key = sg.popup_get_text(str(f"{initial_key} is not a valid product key for "
                                                                f"{row[1].Vendor}, Serial Number: {row[1].Serial_Number}"))
                                while serial_formatter.pk_checker(row, try_key) != row and try_key is not None:
                                    try_key = sg.popup_get_text(str(f"{try_key} is not a valid product key for "
                                                                    f"{row[1].Vendor}, Serial Number: {row[1].Serial_Number}"))
                                row_pk_mod = row[1]._replace(Product_Key=try_key)  # enumeration discarded
                                pk_set_out.add(row_pk_mod)
                            else:
                                row_pk_mod = row[1]._replace(Product_Key=initial_key)  # enumeration discarded
                                pk_set_out.add(row_pk_mod)
                    add_pk_window.Element('UPDATE').Update(["Updated Items:"] + [f"Vendor: {row.Vendor}, Serial Number: "
                                                            f"{row.Serial_Number}, Product Key: {row.Product_Key}" for
                                                            row in pk_set_out])
                    print("pk_set_out post-mod:", pk_set_out)  # for testing purposes
                    # TODO: overwrite rows in db with pk_set_out rows
                    pk_set_out = set()  # empty the set for re-use

        if event == 'Update Software Vendor':
            vendor_buttons = [sg.Button(vendor, size=(max(len(vendor) for vendor in sam_db.view_vendors()), 1),)
                              for vendor in sam_db.view_vendors()]
            usv_layout = [[sg.Text("Select a vendor to modify")]]
            # append buttons to usv_layout in a set number per gui row:
            grid_width = 9
            i = 0
            j = grid_width
            while sum([len(sublists) for sublists in usv_layout])-1 < len(vendor_buttons):
                sublist = vendor_buttons[i:j]
                usv_layout.append(sublist)
                i += grid_width
                j += grid_width
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
                        usv_confirm_layout = [[sg.Text(f"ARE YOU SURE YOU WANT TO CHANGE {usv_event} TO {usv_vendor}?")],
                                               [sg.Button('Yes'), sg.Button('No')]]
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

