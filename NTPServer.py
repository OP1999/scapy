from numpy import float128
from scapy.all import *
import socket
import datetime
import NTPMethods
import PySimpleGUI as sg

localIP = "127.0.0.1"
localPort = 20005
destinationPort = 50005
bufferSize = 1024

# Create a UDP socket at Server side
NTPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
NTPServerSocket.bind((localIP, localPort))
print("NTP Server up and Listening")

# textToSend = "hello client"
# ntpMessage = ""
ntpMode = 1

def read_text_from_file(fileName):
    with open(fileName) as f:
        readFile = f.readlines()
    textToSend = readFile[0]
    convert_text_to_ascii(textToSend)    

def read_image_from_file(fileName):
    with open(fileName) as f:
        readFile = f.readlines()
    textToSend = readFile[0]
    convert_text_to_ascii(textToSend)    

def convert_text_to_ascii(text):
    ascii_values = [ord(character) for character in text]
    # send_custom_packet(ascii_values)
    receive_client_packet(ascii_values)

def receive_client_packet():
    ntpMessage = ""
    while(ntpMode == 1): 
        bytesAddressPair = NTPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]

        answer = NTPMethods.NTPPacket()
        answer = NTPMethods.unpack(answer, message, 1)
        messageLength = NTPMethods.get_message_length(answer)
        print('Message Length: ' + str(messageLength))
        
        # Runs for the length of the message it is receiving / sending
        for i in range(messageLength):
            bytesAddressPair = NTPServerSocket.recvfrom(bufferSize)
            
            # Replies 'R' to show letter is received
            recTimeWithMessage = float128(str(datetime.datetime.timestamp(datetime.datetime.utcnow()))[:-3] + "082") + NTPMethods.date_diff
            
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]

            # clientIP = "Client IP Address:{}".format(address)   
            # print(clientIP)

            answer = NTPMethods.NTPPacket()
            answer = NTPMethods.unpack(answer, message, 1)
            ntpResponse = NTPMethods.to_display(answer)
            character = NTPMethods.get_message(answer)
            
            # Reply Custom Message
            # try:
            #     if(ascii_values[i] < 100):
            #         recTimeWithMessage = float128(str(datetime.datetime.timestamp(datetime.datetime.utcnow()))[:-3] + "0" + str(ascii_values[i])) + NTPMethods.date_diff
            #     else :
            #         recTimeWithMessage = float128(str(datetime.datetime.timestamp(datetime.datetime.utcnow()))[:-3] + str(ascii_values[i])) + NTPMethods.date_diff
            # except:
            #     recTimeWithMessage = float128(str(datetime.datetime.timestamp(datetime.datetime.utcnow()))[:-3] + "032") + NTPMethods.date_diff
                
            returnPacket = IP(dst=address[0])/UDP(sport=localPort,dport=address[1])/NTP(version=4, mode='server', recv=recTimeWithMessage)
            send(returnPacket)

            print(ntpResponse)

            ntpMessage += character
        
        if(len(ntpMessage) == messageLength):
            # Writes NTP Message to a text file and displays a pop up with the message
            with open("NTPServerMessage.txt", "w") as text_file:
                print(f"{ntpMessage}", file=text_file)
        
            sg.popup("Message:", ntpMessage, "Successfully received from client")
        
        # Prints message received via 
        print(ntpMessage)
        ntpMessage = ""

        # ntpMode = 0

        # time.sleep(5)   
        # NTPServerSocket.close()

# ----------- Create the 4 layouts this Window will display -----------
layoutReceive = [   [sg.Text("Server in NTP Receive Mode")],
                    [sg.Text("Message Received: ")]    ]

layoutButtons = [   [sg.Button('Message'), sg.Button('Text File'), sg.Button('Image File')]]

layout1 = [ [sg.Text("Input the message you would like to send to the server")],
            [sg.Input(key="-IN1-")]    ]

layout2 = [ [sg.Text('Send Text File via NTP')],
            [sg.Text("Choose a file: "), sg.Input(key="-IN2-", change_submits=True), sg.FileBrowse(key="-INFile-", file_types=(("Text Files", "*.txt")))] ]
            
layout3 = [ [sg.Text('Send Image via NTP')],
            [sg.Text("Choose a file: "), sg.Input(key="-IN3-", change_submits=True), sg.FileBrowse(key="-INImage-", file_types=(("Image Files", "*.jpg")))] ]

# ----------- Create actual layout using Columns and a row of Buttons
layout = [  [sg.Text('Send via NTP')],
            [sg.Button('Receive Mode'), sg.Button('Send Mode')],
            [sg.Column(layoutButtons, key='-COLButtons-', visible=False)],
            [sg.Column(layoutReceive, key='-COLReceive-')],
            [sg.Column(layout1, visible=False, key='-COL1-'), sg.Column(layout2, visible=False, key='-COL2-'), sg.Column(layout3, visible=False, key='-COL3-')],
            [sg.Button('Send'), sg.Button('Exit')]    ]

window = sg.Window('Send / Receive Data via NTP', layout, size=(500,250), element_justification='c')

# The current layout
sendLayout = 1
while True:
    event, values = window.read()
    # print(event, values)
    if event in (None, 'Exit'):
        break
    if ntpMode == 0:
        window[f'-COLButtons-'].update(visible=False)  
        window[f'-COLReceive-'].update(visible=False)  
    if event == 'Send Mode':
        ntpMode = 2
        window[f'-COLButtons-'].update(visible=True)  
        # send_receive_client_packet()
        window[f'-COLReceive-'].update(visible=False)
        window[f'-COL2-'].update(visible=False)
        window[f'-COL3-'].update(visible=False)
        window[f'-COL1-'].update(visible=True) 
    elif event == 'Receive Mode':
        ntpMode = 1
        # receive_client_packet()
        window[f'-COLButtons-'].update(visible=False)  
        window[f'-COL3-'].update(visible=False)
        window[f'-COL2-'].update(visible=False)  
        window[f'-COL1-'].update(visible=False)
        window[f'-COLReceive-'].update(visible=True)  
    if ntpMode == 2:
        if event == 'Message':
            layout = 1
            window[f'-COL2-'].update(visible=False)
            window[f'-COL3-'].update(visible=False)
            window[f'-COL1-'].update(visible=True)  
        elif event in 'Text File':
            layout = 2
            window[f'-COL1-'].update(visible=False)
            window[f'-COL3-'].update(visible=False)
            window[f'-COL2-'].update(visible=True)
        elif event in 'Image File':
            layout = 3
            window[f'-COL1-'].update(visible=False)
            window[f'-COL2-'].update(visible=False)
            window[f'-COL3-'].update(visible=True)
    if event == "Send":
        if sendLayout == 1:
            convert_text_to_ascii(values["-IN1-"])
        elif sendLayout == 2:
            read_text_from_file(values["-IN2-"])
        elif sendLayout == 3:
            read_image_from_file(values["-IN3-"])
window.close()