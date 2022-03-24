import zipfile
from numpy import float128
from scapy.all import *
import socket
import datetime
import NTPMethods
import PySimpleGUI as sg
import io
from PIL import Image

localIP = "127.0.0.1"
localPort = 20005
destinationIP = "127.0.0.1"
destinationPort = 50005
bufferSize = 1024

# Create a UDP socket at Server side
NTPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
NTPServerSocket.bind((localIP, localPort))
print("NTP Server Up")

global ntpMode
global ntpMessage
global ntpArray

ntpMessage = ""
ntpArray = []

def get_ntp_packet(type):
    bytesAddressPair = NTPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]

    answer = NTPMethods.NTPPacket()
    answer = NTPMethods.unpack(answer, message, type)

    return answer

def receive_client_packet():
    global ntpMode
    while(ntpMode == 1): 
        print("NTP Server Listening Active")
        answer = get_ntp_packet(1)
        messageType = NTPMethods.get_message_type(answer)

        get_message_len(messageType)
        
        ntpMode = 0 

def get_message_len(type):
    answer = get_ntp_packet(4)
    arrayLength = NTPMethods.get_message_length(answer)

    if(type == 1):
        receive_text_packet(arrayLength)
    elif(type == 2):
        receive_byte_packet(arrayLength, 2)
    elif(type == 3):
        receive_byte_packet(arrayLength, 3)

def receive_text_packet(messageLength):
    global ntpMessage
    ntpMessage = ""
    # Runs for the length of the message it is receiving
    for i in range(messageLength):
        # message = bytesAddressPair[0]
        # address = bytesAddressPair[1]

        # # clientIP = "Client IP Address:{}".format(address)   
        # # print(clientIP)


        answer = get_ntp_packet(1)
        # ntpResponse = NTPMethods.to_display(answer)
        character = NTPMethods.get_message_char(answer)

        # Replies 'R' to show letter is received
        recTimeWithMessage = float128(str(datetime.datetime.timestamp(datetime.datetime.utcnow()))[:-3] + "082") + NTPMethods.date_diff
        
           
        # returnPacket = IP(dst=address[0])/UDP(sport=localPort,dport=address[1])/NTP(version=4, mode='server', recv=recTimeWithMessage)
        returnPacket = IP(dst=destinationIP)/UDP(sport=localPort,dport=destinationPort)/NTP(version=4, mode='server', recv=recTimeWithMessage)
        send(returnPacket)

        # print(ntpResponse)
        ntpMessage += character
    
    if(len(ntpMessage) == messageLength):
        # Writes NTP Message to a text file and displays a pop up with the message
        with open("NTPServerMessage.txt", "w") as text_file:
            print(f"{ntpMessage}", file=text_file)

def receive_byte_packet(byteLength, type):
    global ntpArray
    global ntpMessage
    ntpArray = []
    ntpMessage = ""
    # Runs for the length of the message it is receiving
    for i in range(byteLength):
        answer = get_ntp_packet(1)
        # ntpResponse = NTPMethods.to_display(answer)
        character = NTPMethods.get_byte_digit(answer)
        # print(ntpResponse)

        ntpArray.append(character)

    if(type == 2):
        if(len(ntpArray) == byteLength):
            # Writes NTP Message to a png file and displays a pop up with the image
            byteArray = bytearray(ntpArray)
            
            image = Image.open(io.BytesIO(byteArray))
            image.save("NTPServerImg.jpg")

            ntpMessage = "Image"
            # image.show()
    elif(type == 3):
        if(len(ntpArray) == byteLength):
            # Writes NTP Message to a zip file
            byteArray = bytearray(ntpArray)

            with open("NTPServerZip.zip", 'wb') as zip_file:
                zip_file.write(byteArray)

        ntpMessage = "Zip"

# ----------- Create the 5 layouts this Window will display -----------
layoutReceive = [   [sg.Text("Server in NTP Receive Mode")]     ]

layoutSuccReceive = [   [sg.Text("Server successfully Received a Response")],
                        [sg.Text(key="-NTPText-")]    ]

layoutButtons = [   [sg.Button('Message'), sg.Button('Text File'), sg.Button('Image File')]]

layout1 = [ [sg.Text("Input the message you would like to send to the server")],
            [sg.Input(key="-IN1-")]    ]

layout2 = [ [sg.Text('Send Text File via NTP')],
            [sg.Text("Choose a file: "), sg.Input(key="-IN2-", change_submits=True), sg.FileBrowse(key="-INFile-", file_types=(("Text Files", "*.txt")))] ]
            
layout3 = [ [sg.Text('Send Image via NTP')],
            [sg.Text("Choose a file: "), sg.Input(key="-IN3-", change_submits=True), sg.FileBrowse(key="-INImage-", file_types=(("Image Files", "*.jpg")))] ]

# ----------- Create actual layout using Columns and a row of Buttons
winLayout = [  [sg.Text('Send / Receive via NTP')],
            [sg.Button('Receive Mode'), sg.Button('Send Mode')],
            [sg.Column(layoutReceive, key='-COLReceive-', visible=False)],
            [sg.Column(layoutSuccReceive, key='-COLSuccReceive-', visible=False)],
            [sg.Column(layoutButtons, key='-COLButtons-', visible=False)],
            [sg.Column(layout1, visible=False, key='-COL1-'), sg.Column(layout2, visible=False, key='-COL2-'), sg.Column(layout3, visible=False, key='-COL3-')],
            [sg.Button('Send', key='-SendButton-', visible=False), sg.Button('Exit')]    ]

window = sg.Window('Send / Receive Data via NTP', winLayout, size=(500,300), element_justification='c')

layout = 1
while True:
    event, values = window.read()
    # print(event, values)
    if event in (None, 'Exit'):
        NTPServerSocket.close()
        break
    if event == 'Receive Mode':
        ntpMode = 1
        window[f'-SendButton-'].update(visible=False)  
        window[f'-COLButtons-'].update(visible=False) 
        window[f'-COLSuccReceive-'].update(visible=False)
        window[f'-COLReceive-'].update(visible=True)  
        window[f'-COL3-'].update(visible=False)
        window[f'-COL2-'].update(visible=False)  
        window[f'-COL1-'].update(visible=False)
        window.refresh()
        receive_client_packet() 
        window.refresh()
    elif event == 'Send Mode':
        ntpMode = 2
        window[f'-COLReceive-'].update(visible=False)
        window[f'-COLSuccReceive-'].update(visible=False)
        window[f'-SendButton-'].update(visible=True)  
        window[f'-COLButtons-'].update(visible=True)         
        window[f'-COL2-'].update(visible=False)
        window[f'-COL3-'].update(visible=False)
        window[f'-COL1-'].update(visible=True)
        window.refresh()
        # send_receive_client_packet()  
    if ntpMode == 0:
        window[f'-NTPText-'].update('Message Received: ' + ntpMessage)
        window[f'-COLButtons-'].update(visible=False)  
        window[f'-COLReceive-'].update(visible=False)
        window[f'-SendButton-'].update(visible=False)  
        window[f'-COLSuccReceive-'].update(visible=True)
        window.bring_to_front()
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
    # if event == "Send":
        # if layout == 1:
        #     convert_text_to_ascii(values["-IN1-"])
        # elif layout == 2:
        #     read_text_from_file(values["-IN2-"])
        # elif layout == 3:
        #     read_image_from_file(values["-IN3-"])
window.close()