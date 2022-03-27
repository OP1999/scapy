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
winLayout = [   [sg.Text(key='-NTPType-')],
            [sg.Button('Receive Mode'), sg.Button('Send Mode')],
            [sg.Column(layoutReceive, key='-COLReceive-', visible=False)],
            [sg.Column(layoutButton, key='-COLBtn-', visible=False)],
            [sg.Column(layoutMes, visible=False, key='-COLMes-'), sg.Column(layoutTxt, visible=False, key='-COLTxt-'), sg.Column(layoutImg, visible=False, key='-COLImg-'), sg.Column(layoutZip, visible=False, key='-COLZip-')],
            [sg.Column(layoutResponse, key='-COLResponse-', visible=False)],
            [sg.Button('Send', key='-BTNSend-', visible=False)], 
            [sg.Button('Exit', key='-BTNExit-')]    ]

def clear_columns(window):
    window[f'-COLMes-'].update(visible=False)
    window[f'-COLTxt-'].update(visible=False)
    window[f'-COLZip-'].update(visible=False)
    window[f'-COLImg-'].update(visible=False)

def clear_text(window):
    window[f'-INMes-'].update("")
    window[f'-INTxt-'].update("")
    window[f'-INImg-'].update("")
    window[f'-INZip-'].update("")

def gui_window(window, event, values, NTPSocket, destinationIP, localPort, destinationPort, NTPType):
    global layout
    global ntpMode
    global ntpMessage
    global response
    if event == "-BTNSend-":
        if layout == 1:
            response = NTPMethods.send_text_packet(NTPSocket, NTPMethods.send_text(values["-INMes-"], destinationIP, localPort, destinationPort, NTPType), destinationIP, localPort, destinationPort, NTPType)
        if layout == 2:
            textToSend = NTPMethods.read_text_from_file(values["-INTxt-"], destinationIP, localPort, destinationPort, NTPType)
            if textToSend == 6:
                layout = 6
                ntpMode = 3
            else:
                response = NTPMethods.send_text_packet(NTPSocket, textToSend, destinationIP, localPort, destinationPort, NTPType)
        if layout == 3:
            byteToSend = NTPMethods.read_image_from_file(values["-INImg-"], destinationIP, localPort, destinationPort, NTPType)
            if byteToSend == 6:
                layout = 6
                ntpMode = 3
            else:
                response = NTPMethods.send_byte_packet(NTPSocket, byteToSend, destinationIP, localPort, destinationPort, NTPType)
        if layout == 4:
            byteToSend = NTPMethods.read_zip_from_file(values["-INZip-"], destinationIP, localPort, destinationPort, NTPType)
            if byteToSend == 6:
                layout = 6
                ntpMode = 3
            else:
                response = NTPMethods.send_byte_packet(NTPSocket, byteToSend, destinationIP, localPort, destinationPort, NTPType)
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
        window[f'-COLReceive-'].update(visible=True)        
        window.refresh()
        response = NTPMethods.receive_packet(NTPSocket, destinationIP, localPort, destinationPort, NTPType) 
        ntpMessage = response[0]
        ntpMode = response[1]
        window.refresh()
    elif event == 'Send Mode':
        ntpMessage = ""
        layout = 1
        ntpMode = 2
        clear_columns(window)
        clear_text(window)
        window[f'-COLResponse-'].update(visible=False) 
        window[f'-COLReceive-'].update(visible=False)  
        window[f'-COLBtn-'].update(visible=True) 
        window[f'-COLMes-'].update(visible=True) 
        window[f'-BTNSend-'].update(visible=True)    
        window.refresh()
    if ntpMode == 0:
        window[f'-Mess-'].update(NTPType + " successfully Received a Message")
        window[f'-NTPText-'].update('Message Received: ' + ntpMessage)
        clear_text(window)
        clear_columns(window)
        window[f'-COLBtn-'].update(visible=False)
        window[f'-COLReceive-'].update(visible=False) 
        window[f'-COLResponse-'].update(visible=True)
        window.bring_to_front()
        window.refresh()
        ntpMessage = ""
    elif ntpMode == 2:
        if event == 'Message':
            layout = 1
            window[f'-COLTxt-'].update(visible=False)
            window[f'-COLImg-'].update(visible=False)
            window[f'-COLZip-'].update(visible=False)
            window[f'-COLMes-'].update(visible=True)  
        elif event in 'Text File':
            layout = 2
            window[f'-COLMes-'].update(visible=False)
            window[f'-COLImg-'].update(visible=False)
            window[f'-COLZip-'].update(visible=False)
            window[f'-COLTxt-'].update(visible=True)
        elif event in 'Image File':
            layout = 3
            window[f'-COLMes-'].update(visible=False)
            window[f'-COLTxt-'].update(visible=False)
            window[f'-COLZip-'].update(visible=False)
            window[f'-COLImg-'].update(visible=True)
        elif event in 'Zip File':
            layout = 4
            window[f'-COLMes-'].update(visible=False)
            window[f'-COLTxt-'].update(visible=False)
            window[f'-COLImg-'].update(visible=False)
            window[f'-COLZip-'].update(visible=True)
    elif ntpMode == 3:    
        if layout == 5:
            window[f'-Mess-'].update(NTPType + " successfully Sent a Message")
            window[f'-NTPText-'].update('Message Sent of size: ' + ntpMessage)
            window[f'-COLResponse-'].update(visible=True)
            window[f'-COLBtn-'].update(visible=False) 
            window[f'-BTNSend-'].update(visible=False)
            clear_columns(window)
        elif layout == 6:
            window[f'-Mess-'].update("Unsuccessful Sending File")
            window[f'-NTPText-'].update('Wrong File Type - Please choose again')
            window[f'-COLResponse-'].update(visible=True)
            window[f'-COLBtn-'].update(visible=False) 
            window[f'-BTNSend-'].update(visible=False)
            clear_columns(window)