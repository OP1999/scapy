import PySimpleGUI as sg
import NTPMethods

global layout
global ntpMode
global ntpMessage
global response

ntpMode = 0
layout = 1
ntpMessage = ""

# ----------- Create the layouts this Window will display -----------
layoutNTPBtns = [   [sg.Button('Receive Mode'), sg.Button('Send Mode')]    ]

layoutReceive = [   [sg.Text("NTP Receive Mode")]     ]

layoutResponse = [   [sg.Text(key="-Mess-")],
                        [sg.Text(key="-NTPText-")]    ]

layoutButton = [    [sg.Button('Message'), sg.Button('Text File'), sg.Button('Image File'), sg.Button('Zip File')]    ]

layoutMes = [ [sg.Text("Input the message you would like to send to the server")],
            [sg.Input(key="-INMes-")]    ]

layoutTxt = [ [sg.Text('Send Text File via NTP')],
            [sg.Text("Choose a file: "), sg.Input(key="-INTxt-", change_submits=True), sg.FileBrowse(key="-INFBTxt-", file_types=(("Text Files", "*.txt")))] ]
            
layoutImg = [ [sg.Text('Send Image via NTP')],
            [sg.Text("Choose a file: "), sg.Input(key="-INImg-", change_submits=True), sg.FileBrowse(key="-INFBImage-", file_types=(("Image Files", "*.jpg")))] ]

layoutZip = [ [sg.Text('Send Zip via NTP')],
            [sg.Text("Choose a file: "), sg.Input(key="-INZip-", change_submits=True), sg.FileBrowse(key="-INFBZip-", file_types=(("Zip Files", "*.zip")))] ]

# ----------- Create actual layout using Columns and a row of Buttons
winLayout = [   [sg.Column(layoutNTPBtns, key='-COLNTPBtns-')],
            [sg.Column(layoutReceive, key='-COLReceive-', visible=False)],
            [sg.Column(layoutButton, key='-COLBtn-', visible=False)],
            [sg.Column(layoutMes, visible=False, key='-COLMes-'), sg.Column(layoutTxt, visible=False, key='-COLTxt-'), sg.Column(layoutImg, visible=False, key='-COLImg-'), sg.Column(layoutZip, visible=False, key='-COLZip-')],
            [sg.Column(layoutResponse, key='-COLResponse-', visible=False)],
            [sg.Button('Send', key='-BTNSend-', visible=False)], 
            [sg.Button('Exit', key='-BTNExit-')]    ]

centredLayout = [  [sg.VPush()],
            [sg.Push(), sg.Column(winLayout, element_justification='c'), sg.Push()],
            [sg.VPush()]    ]

def clear_columns(window):
    window[f'-COLMes-'].update(visible=False)
    window[f'-COLTxt-'].update(visible=False)
    window[f'-COLZip-'].update(visible=False)
    window[f'-COLImg-'].update(visible=False)
    window[f'-COLMes-'].hide_row() 

def clear_text(window):
    window[f'-INMes-'].update("")
    window[f'-INTxt-'].update("")
    window[f'-INImg-'].update("")
    window[f'-INZip-'].update("")

def exit_btn(window):
    window[f'-BTNExit-'].update(visible=False)
    window[f'-BTNExit-'].hide_row() 
    window[f'-BTNExit-'].update(visible=True)
    window[f'-BTNExit-'].unhide_row() 

def send_btn(window):
    window[f'-BTNSend-'].update(visible=False)
    window[f'-BTNSend-'].hide_row() 
    window[f'-BTNSend-'].update(visible=True)
    window[f'-BTNSend-'].unhide_row() 

def gui_window(window, event, values, NTPSocket, destinationIP, localPort, destinationPort, NTPType):
    global layout
    global ntpMode
    global ntpMessage
    global response
    if event == "-BTNSend-":
        response = 0
        if layout == 1:
            if values["-INMes-"] != "":
                response = NTPMethods.send_text_packet(NTPSocket, NTPMethods.send_text(values["-INMes-"], destinationIP, localPort, destinationPort, NTPType), destinationIP, localPort, destinationPort, NTPType)
            else:
                sg.Popup('Enter a Message to Send')
        elif layout == 2:
            if values["-INTxt-"] != "":
                textToSend = NTPMethods.read_text_from_file(values["-INTxt-"], destinationIP, localPort, destinationPort, NTPType)
                if textToSend == 6:
                    layout = 6
                    ntpMode = 3
                else:
                    response = NTPMethods.send_text_packet(NTPSocket, textToSend, destinationIP, localPort, destinationPort, NTPType)
            else:
                sg.Popup('Select a file to Send')
        elif layout == 3:
            if values["-INImg-"] != "":
                byteToSend = NTPMethods.read_image_from_file(values["-INImg-"], destinationIP, localPort, destinationPort, NTPType)
                if byteToSend == 6:
                    layout = 6
                    ntpMode = 3 
                else:
                    response = NTPMethods.send_byte_packet(NTPSocket, byteToSend, destinationIP, localPort, destinationPort, NTPType)
            else:
                sg.Popup('Select a file to Send')
        elif layout == 4:
            if values["-INZip-"] != "":
                byteToSend = NTPMethods.read_zip_from_file(values["-INZip-"], destinationIP, localPort, destinationPort, NTPType)
                if byteToSend == 6:
                    layout = 6
                    ntpMode = 3                    
                else:
                    response = NTPMethods.send_byte_packet(NTPSocket, byteToSend, destinationIP, localPort, destinationPort, NTPType)
            else:
                sg.Popup('Select a file to Send')
        if(response != 0):
            ntpMessage = response[0]
            layout = response[1]
            ntpMode = response[2]
    if event == 'Receive Mode':
        ntpMessage = ""
        layout = 0
        ntpMode = 1
        window[f'-COLBtn-'].update(visible=False) 
        clear_columns(window)
        window[f'-COLResponse-'].update(visible=False) 
        window[f'-BTNSend-'].update(visible=False) 
        window[f'-COLNTPBtns-'].update(visible=False) 
        window[f'-COLBtn-'].hide_row() 
        window[f'-COLResponse-'].hide_row() 
        window[f'-BTNSend-'].hide_row()
        window[f'-COLNTPBtns-'].hide_row() 
        window[f'-COLReceive-'].update(visible=True)    
        window[f'-COLReceive-'].unhide_row()
        exit_btn(window)     
        window.refresh()
        response = NTPMethods.receive_packet(NTPSocket, destinationIP, localPort, destinationPort, NTPType) 
        ntpMessage = response[0]
        ntpMode = response[1]
        exit_btn(window)
        window.refresh()
    elif event == 'Send Mode':
        ntpMessage = ""
        layout = 1
        ntpMode = 2
        clear_columns(window)
        clear_text(window)
        window[f'-COLResponse-'].update(visible=False) 
        window[f'-COLReceive-'].update(visible=False)  
        window[f'-COLResponse-'].hide_row()
        window[f'-COLReceive-'].hide_row()  
        window[f'-COLBtn-'].update(visible=True)
        window[f'-COLMes-'].update(visible=True)
        window[f'-BTNSend-'].update(visible=True) 
        window[f'-COLBtn-'].unhide_row() 
        window[f'-COLMes-'].unhide_row()  
        window[f'-BTNSend-'].unhide_row() 
        send_btn(window)
        exit_btn(window)
        window.refresh()
    if ntpMode == 0:
        window[f'-Mess-'].update(NTPType + " successfully Received a Message")
        window[f'-NTPText-'].update('Message Received: ' + ntpMessage)
        clear_text(window)
        clear_columns(window)
        window[f'-COLBtn-'].update(visible=False)
        window[f'-COLReceive-'].update(visible=False)
        window[f'-COLBtn-'].hide_row() 
        window[f'-COLReceive-'].hide_row() 
        window[f'-COLResponse-'].update(visible=True)
        window[f'-COLNTPBtns-'].update(visible=True) 
        window[f'-COLResponse-'].unhide_row() 
        window[f'-COLNTPBtns-'].unhide_row() 
        exit_btn(window)
        window.refresh()
        ntpMessage = ""
    elif ntpMode == 2:
        if event == 'Message':
            layout = 1
            window[f'-COLTxt-'].update(visible=False)
            window[f'-COLImg-'].update(visible=False)
            window[f'-COLZip-'].update(visible=False)
            window[f'-COLMes-'].update(visible=True)  
            window[f'-COLMes-'].unhide_row() 
        elif event in 'Text File':
            layout = 2
            window[f'-COLMes-'].update(visible=False)
            window[f'-COLImg-'].update(visible=False)
            window[f'-COLZip-'].update(visible=False)
            window[f'-COLTxt-'].update(visible=True)
            window[f'-COLTxt-'].unhide_row() 
        elif event in 'Image File':
            layout = 3
            window[f'-COLMes-'].update(visible=False)
            window[f'-COLTxt-'].update(visible=False)
            window[f'-COLZip-'].update(visible=False)
            window[f'-COLImg-'].update(visible=True)
            window[f'-COLImg-'].unhide_row() 
        elif event in 'Zip File':
            layout = 4
            window[f'-COLMes-'].update(visible=False)
            window[f'-COLTxt-'].update(visible=False)
            window[f'-COLImg-'].update(visible=False)
            window[f'-COLZip-'].update(visible=True)
            window[f'-COLZip-'].unhide_row() 
        send_btn(window)
        exit_btn(window)
    elif ntpMode == 3:    
        if layout == 5:
            window[f'-Mess-'].update(NTPType + " successfully Sent a Message")
            window[f'-NTPText-'].update('Message Sent of size: ' + ntpMessage)
            window[f'-COLNTPBtns-'].update(visible=True) 
            window[f'-COLResponse-'].update(visible=True)
            window[f'-COLNTPBtns-'].unhide_row() 
            window[f'-COLResponse-'].unhide_row() 
            window[f'-COLBtn-'].update(visible=False) 
            window[f'-BTNSend-'].update(visible=False)
            window[f'-COLBtn-'].hide_row() 
            window[f'-BTNSend-'].hide_row() 
            clear_columns(window)
        elif layout == 6:
            window[f'-Mess-'].update("Unsuccessful Sending File")
            window[f'-NTPText-'].update('Wrong File Type - Please choose again')
            window[f'-COLNTPBtns-'].update(visible=True) 
            window[f'-COLResponse-'].update(visible=True)
            window[f'-COLNTPBtns-'].unhide_row() 
            window[f'-COLResponse-'].unhide_row() 
            window[f'-COLBtn-'].update(visible=False) 
            window[f'-BTNSend-'].update(visible=False)
            window[f'-COLBtn-'].hide_row() 
            window[f'-BTNSend-'].hide_row()
            clear_columns(window)
        exit_btn(window)