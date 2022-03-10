import PySimpleGUI as sg

# ----------- Create the 3 layouts this Window will display -----------
layout1 = [ [sg.Text("Input the message you would like to send to the server")],
            [sg.Input(key="-IN1-")]    ]

layout2 = [ [sg.Text('Send Text File via NTP')],
            [sg.Text("Choose a file: "), sg.Input(key="-IN2-", change_submits=True), sg.FileBrowse(key="-INFile-", file_types=(("Text Files", "*.txt")))] ]
            
layout3 = [ [sg.Text('Send Image via NTP')],
            [sg.Text("Choose a file: "), sg.Input(key="-IN3-", change_submits=True), sg.FileBrowse(key="-INImage-", file_types=(("Image Files", "*.jpg")))] ]

# ----------- Create actual layout using Columns and a row of Buttons
layout = [  [sg.Text('Send via NTP')],
            [sg.Button('Text'), sg.Button('Image'), sg.Button('File')],
            [sg.Column(layout1, key='-COL1-'), sg.Column(layout2, visible=False, key='-COL2-'), sg.Column(layout3, visible=False, key='-COL3-')],
            [sg.Button('Send'), sg.Button('Exit')]    ]

window = sg.Window('Send Data via NTP', layout, size=(500,150), element_justification='c')

layout = 1  # The currently visible layout
while True:
    event, values = window.read()
    # print(event, values)
    if event in (None, 'Exit'):
        break
    if event == "Send":
        if layout == 1:
            print(values["-IN1-"])
        if layout == 2:
            print(values["-IN2-"])
        if layout == 3:
            print(values["-IN3-"])
    if event == 'Text':
        layout = 1
        window[f'-COL2-'].update(visible=False)
        window[f'-COL3-'].update(visible=False)
        window[f'-COL1-'].update(visible=True)  
    elif event in 'Image':
        layout = 2
        window[f'-COL1-'].update(visible=False)
        window[f'-COL3-'].update(visible=False)
        window[f'-COL2-'].update(visible=True)
    elif event in 'File':
        layout = 3
        window[f'-COL1-'].update(visible=False)
        window[f'-COL2-'].update(visible=False)
        window[f'-COL3-'].update(visible=True)
window.close()