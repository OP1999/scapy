import PySimpleGUI as sg

def gui_windows(text, window, button, response):
    # Window allowing the user to choose whether to send or receive a message with a client
    layout = [  [sg.Text(text)],
                [sg.Input()],
                [sg.Button(button)] ]

    window = sg.Window(window, layout)
                                                    
    event, values = window.read()

    print("Success! '", values[0], response)

    window.close()
    return values