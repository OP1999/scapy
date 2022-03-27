import PySimpleGUI as sg

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