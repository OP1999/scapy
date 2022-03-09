import PySimpleGUI as sg

# ----------- Create the 3 layouts this Window will display -----------
layout1 = [ [sg.Text("Input the message you would like to send to the server")],
            [sg.Input()]    ]

layout2 = [ [sg.Text('Send File via NTP')],
            [sg.Text("Choose a file: "), sg.Input(key="-IN2-", change_submits=True), sg.FileBrowse(key="-IN-")] ]
            
layout3 = [ [sg.Text('Send Image via NTP')],
            [sg.Text("Choose a file: "), sg.Input(key="-IN3-", change_submits=True), sg.FileBrowse(key="-IN-")] ]

# ----------- Create actual layout using Columns and a row of Buttons
layout = [  [sg.Text('Send via NTP')],
            [sg.Button('Text'), sg.Button('Image'), sg.Button('File')],
            [sg.Column(layout1, key='-COL1-'), sg.Column(layout2, visible=False, key='-COL2-'), sg.Column(layout3, visible=False, key='-COL3-')],
            [sg.Button('Send'), sg.Button('Exit')]    ]

window = sg.Window('Send Data via NTP', layout, size=(500,150), element_justification='c')

layout = 1  # The currently visible layout
while True:
    event, values = window.read()
    print(event, values)
    if event in (None, 'Exit'):
        break
    if event == 'Text':
        window[f'-COL2-'].update(visible=False)
        window[f'-COL3-'].update(visible=False)
        window[f'-COL1-'].update(visible=True)  
    elif event in 'Image':
        window[f'-COL1-'].update(visible=False)
        window[f'-COL3-'].update(visible=False)
        window[f'-COL2-'].update(visible=True)
    elif event in 'File':
        window[f'-COL1-'].update(visible=False)
        window[f'-COL2-'].update(visible=False)
        window[f'-COL3-'].update(visible=True)
window.close()

# def gui_windows(text, window, button, response):
#     # Window allowing the user to choose whether to send or receive a message with a client
#     layout = [  [sg.Text(text)],
#                 [sg.Input()],
#                 [sg.Button(button)] ]

#     window = sg.Window(window, layout)
                                                    
#     event, values = window.read()

#     print("Success! '", values[0], response)

#     window.close()
#     return values

# sg.theme("DarkTeal2")
# layout = [  [sg.T("")], 
#             [sg.Text("Choose a folder: "), 
#             sg.Input(key="-IN2-", change_submits=True), 
#             sg.FolderBrowse(key="-IN-")],
#             [sg.Button("Submit")]]

# ###Building Window
# window = sg.Window('File Browser', layout, size=(600,150))
    
# while True:
#     event, values = window.read()
#     print(values["-IN2-"])
#     if event == sg.WIN_CLOSED or event=="Exit":
#         break
#     elif event == "Submit":
#         print(values["-IN-"])

# layout = [[sg.Button("Text"), sg.Button("Image"), sg.Button("File")], [sg.Text("Choose a file: "), sg.Input(key="-IN2-", change_submits=True), sg.FileBrowse(key="-IN-")],[sg.Button("Submit"), sg.Button("Exit")]]

# ###Building Window
# window = sg.Window('Send Data via NTP', layout, size=(500,150), element_justification='c')
    
# while True:
#     event, values = window.read()
#     if event == sg.WIN_CLOSED or event=="Exit":
#         break
#     elif event == "Submit":
#         print(values["-IN-"])