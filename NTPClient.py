from numpy import float128
from scapy.all import *
import socket
import NTPMethods
import PySimpleGUI as sg
import os.path

localIP = NTPMethods.clientIP
localPort = NTPMethods.clientPort
destinationIP = NTPMethods.serverIP
destinationPort = NTPMethods.serverPort

# Create a UDP socket at Client side
NTPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
NTPClientSocket.bind((localIP, localPort))
print("NTP Client Up")

global layout
global ntpMode
global ntpMessage

def read_text_from_file(fileName):
    global layout
    if(os.path.splitext(fileName)[1] == '.docx'):
        send_text(NTPMethods.getTextFromDoc(fileName))
    elif(os.path.splitext(fileName)[1] == '.txt'):
        send_text(NTPMethods.getTextFromTxt(fileName))
    else:
        layout = 5

def read_image_from_file(fileName): 
    global layout
    if(os.path.splitext(fileName)[1] == '.png'):
        with open(fileName, "rb") as image:
            image_values = image.read()
            send_packet(NTPMethods.get_message_value(2))
            send_packet(NTPMethods.get_message_length(len(image_values)))
            send_byte_packet(image_values)
    elif(os.path.splitext(fileName)[1] == '.jpg'):
        with open(fileName, "rb") as image:
            image_values = image.read()
            send_packet(NTPMethods.get_message_value(2))
            send_packet(NTPMethods.get_message_length(len(image_values)))
            send_byte_packet(image_values)
    else:
        layout = 5

def read_zip_from_file(fileName): 
    global layout
    if(os.path.splitext(fileName)[1] == '.zip'):
        with open(fileName, "rb") as zip:
            zip_values = zip.read()
            send_packet(NTPMethods.get_message_value(3))
            send_packet(NTPMethods.get_message_length(len(zip_values)))
            send_byte_packet(zip_values)
    else:
        layout = 5

def send_text(textToSend):
    send_packet(NTPMethods.get_message_value(1))
    ascii_values = NTPMethods.convert_text_to_ascii(textToSend)
    send_packet(NTPMethods.get_message_length(len(ascii_values)))
    send_text_packet(ascii_values)

def send_packet(refTimeWithOffset):
    packet = IP(dst=destinationIP)/UDP(sport=localPort, dport=destinationPort)/NTP(version=4, mode='client', ref=refTimeWithOffset)
    send(packet)

def send_text_packet(int_values):
    global layout
    global ntpMessage
    global ntpMode
    ntpMessage = ""
    # Runs for the length of the message it is sending
    for i in range(len(int_values)):
        send_packet(NTPMethods.get_message_value(int_values[i]))

    ntpMessage = str(receive_message_length())

    # ntpMessage = "Text Sent"

    layout = 0
    ntpMode = 0

    # if(ntpLength == len(int_values)):
    #     # Prints Message Received & Writes it to a text file then closes connection
    #     with open("NTPClientMessage.txt", "w") as text_file:
    #         print(f"{ntpMessage}", file=text_file)

def send_byte_packet(int_values):
    global layout
    global ntpMessage
    global ntpMode
    ntpMessage = ""
    # Runs for the length of the message it is sending
    for i in range(len(int_values)):
        send_packet(NTPMethods.get_message_value(int_values[i]))

    ntpMessage = "Bytes Sent"

    layout = 0
    ntpMode = 0

def receive_message_length():
    bytesAddressPair = NTPClientSocket.recvfrom(NTPMethods.bufferSize)
    message = bytesAddressPair[0]

    answer = NTPMethods.NTPPacket()
    answer = NTPMethods.unpack(answer, message, 2)

    return NTPMethods.get_mess_length(answer)

# ----------- Create the layouts this Window will display -----------
layoutReceive = [   [sg.Text("Server in NTP Receive Mode")]     ]

layoutSuccReceive = [   [sg.Text("Server successfully Received a Response")],
                        [sg.Text(key="-NTPRecText-")]    ]
                    
layoutSuccSent = [  [sg.Text(key="-ErrorMess-")],
                    [sg.Text(key="-NTPSentText-")]    ]

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
winLayout = [   [sg.Text('Client')],
            [sg.Button('Receive Mode'), sg.Button('Send Mode')],
            [sg.Column(layoutReceive, key='-COLReceive-', visible=False)],
            [sg.Column(layoutButton, key='-COLBtn-', visible=False)],
            [sg.Column(layoutSuccReceive, key='-COLSuccReceive-', visible=False)],
            [sg.Column(layoutMes, visible=False, key='-COLMes-'), sg.Column(layoutTxt, visible=False, key='-COLTxt-'), sg.Column(layoutImg, visible=False, key='-COLImg-'), sg.Column(layoutZip, visible=False, key='-COLZip-')],
            [sg.Column(layoutSuccSent, key='-COLSuccSent-', visible=False)],
            [sg.Button('Send', key='-BTNSend-', visible=False)], 
            [sg.Button('Exit', key='-BTNExit-')]    ]
window = sg.Window('Send / Receive Data via NTP', winLayout, size=(500,300), element_justification='c')

layout = 1  # The currently visible layout
while True:
    event, values = window.read()
    # print(event, values)
    if event in (None, '-BTNExit-'):
        NTPClientSocket.close()
        break
    if event == "-BTNSend-":
        if layout == 1:
            send_text(values["-INMes-"])
        if layout == 2:
            read_text_from_file(values["-INTxt-"])
        if layout == 3:
            read_image_from_file(values["-INImg-"])
        if layout == 4:
            read_zip_from_file(values["-INZip-"])
    if event == 'Receive Mode':
        print('Receive')
        ntpMode = 1
        window[f'-COLBtn-'].update(visible=False) 
        window[f'-COLSuccReceive-'].update(visible=False)
        window[f'-COLMes-'].update(visible=False)
        window[f'-COLTxt-'].update(visible=False)  
        window[f'-COLImg-'].update(visible=False)
        window[f'-COLZip-'].update(visible=False) 
        window[f'-COLSuccSent-'].update(visible=False) 
        window[f'-BTNSend-'].update(visible=False) 
        window[f'-COLReceive-'].update(visible=True)        
        window.refresh()
        # receive_client_packet() 
        window.refresh()
    elif event == 'Send Mode':
        print('Send')
        ntpMode = 2
        window[f'-COLSuccReceive-'].update(visible=False)
        window[f'-COLTxt-'].update(visible=False)  
        window[f'-COLImg-'].update(visible=False)
        window[f'-COLZip-'].update(visible=False) 
        window[f'-COLSuccSent-'].update(visible=False) 
        window[f'-COLReceive-'].update(visible=False)  
        window[f'-COLBtn-'].update(visible=True) 
        window[f'-COLMes-'].update(visible=True) 
        window[f'-BTNSend-'].update(visible=True)    
        window.refresh()
    if ntpMode == 0:
        window[f'-ErrorMess-'].update("Client successfully Sent a Message")
        window[f'-NTPSentText-'].update('Server Received Message of Size: ' + ntpMessage)
        window[f'-INMes-'].update("")
        window[f'-INTxt-'].update("")
        window[f'-INImg-'].update("")
        window[f'-INZip-'].update("")
        window[f'-COLMes-'].update(visible=False) 
        window[f'-COLTxt-'].update(visible=False)  
        window[f'-COLImg-'].update(visible=False)
        window[f'-COLZip-'].update(visible=False) 
        window[f'-COLBtn-'].update(visible=False) 
        window[f'-COLSuccSent-'].update(visible=True)
        window.bring_to_front()
        window.refresh()
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
            window[f'-ErrorMess-'].update("Client successfully Sent a Message")
            window[f'-NTPSuccText-'].update('Message Received: ' + ntpMessage)
            window[f'-COLSuccSent-'].update(visible=True)
            window[f'-BTNSend-'].update(visible=False)
            window[f'-COL1-'].update(visible=False)
            window[f'-COL2-'].update(visible=False)
            window[f'-COL3-'].update(visible=False)
            window[f'-COL4-'].update(visible=False)
        elif layout == 6:
            window[f'-ErrorMess-'].update("Unsuccessful Sending File")
            window[f'-NTPRecText-'].update('Wrong File Type - Please choose again')
            window[f'-COLSuccSent-'].update(visible=True)
            window[f'-BTNSend-'].update(visible=False)
            window[f'-COL1-'].update(visible=False)
            window[f'-COL2-'].update(visible=False)
            window[f'-COL3-'].update(visible=False)
            window[f'-COL4-'].update(visible=False)