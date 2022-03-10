from numpy import float128
from scapy.all import *
import socket
import NTPMethods
import datetime
import PySimpleGUI as sg

localIP = "127.0.0.1"
localPort = 50005
destinationPort = 20005
bufferSize = 1024

# Create a UDP socket at Client side
NTPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
NTPClientSocket.bind((localIP, localPort))
print("NTP Client up and listening")

# textToSend = ""
# ascii_values = []
# cryptoKey = 40
ntpMessage = ""

def read_text_from_file(fileName):
    with open(fileName) as f:
        readFile = f.readlines()
    textToSend = readFile[0]
    convert_text_to_ascii(textToSend)    

def read_image_from_file(fileName): 
    with open(fileName, "rb") as image:
        readImage = image.read()
        imageValues = bytearray(readImage)
        # print(imageValues[0])
        send_custom_packet(imageValues)

def convert_text_to_ascii(text):
    ascii_values = [ord(character) for character in text]
    send_custom_packet(ascii_values)

def send_custom_packet(int_values):
    # Sends a packet with the length of the message
    if(len(int_values) < 10):
        refTimeWithOffset = float128(str(datetime.datetime.timestamp(datetime.datetime.utcnow()))[:-3] + "00" + str(len(int_values))) + NTPMethods.date_diff
    else:
        refTimeWithOffset = float128(str(datetime.datetime.timestamp(datetime.datetime.utcnow()))[:-3] + "0" + str(len(int_values))) + NTPMethods.date_diff

    initialPacket = IP(dst=localIP)/UDP(sport=localPort, dport=destinationPort)/NTP(version=4, mode='client', ref=refTimeWithOffset)
    # initialPacket = IP(dst=localIP)/UDP(sport=localPort)/NTP(version=4, mode='client', ref=refTimeWithOffset)
    send(initialPacket)

    send_client_packet(int_values)

def send_client_packet(ascii_values):
# while(True):
    # Runs for the length of the message it is sending
    for i in range(len(ascii_values)):
        if(ascii_values[i] < 100):
            refTimeWithMessage = float128(str(datetime.datetime.timestamp(datetime.datetime.utcnow()))[:-3] + "0" + str(ascii_values[i])) + NTPMethods.date_diff
        else :
            refTimeWithMessage = float128(str(datetime.datetime.timestamp(datetime.datetime.utcnow()))[:-3] + str(ascii_values[i])) + NTPMethods.date_diff

        clientPacket = IP(dst=localIP)/UDP(sport=localPort, dport=destinationPort)/NTP(version=4, mode='client', ref=refTimeWithMessage)
        # clientPacket = IP(dst=localIP)/UDP(sport=localPort)/NTP(version=4, mode='client', ref=refTimeWithMessage)
        send(clientPacket)

        bytesAddressPair = NTPClientSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]

        # serverIP = "Server IP Address:{}".format(address)
        # print(serverIP)

        answer = NTPMethods.NTPPacket()
        answer = NTPMethods.unpack(answer, message, 2)
        ntpResponse = NTPMethods.to_display(answer)
        character = NTPMethods.get_message(answer)

        print(ntpResponse)
        
        # Should Print letter 'R' if message successfully received
        # ntpMessage += character
        # print(ntpMessage)

        time.sleep(1)
    
    # if(len(ntpMessage) == len(ascii_values)):
    #     print(ntpMessage)
    #     # Prints Message Received & Writes it to a text file then closes connection
    #     with open("NTPClientMessage.txt", "w") as text_file:
    #         print(f"{ntpMessage}", file=text_file)

    #     sg.popup("Message successfully sent to the server")

    # print(ntpMessage)
    # time.sleep(5)   
    # NTPClientSocket.close()

# ----------- Create the 3 layouts this Window will display -----------
layout1 = [ [sg.Text("Input the message you would like to send to the server")],
            [sg.Input(key="-IN1-")]    ]

layout2 = [ [sg.Text('Send Text File via NTP')],
            [sg.Text("Choose a file: "), sg.Input(key="-IN2-", change_submits=True), sg.FileBrowse(key="-INFile-", file_types=(("Text Files", "*.txt")))] ]
            
layout3 = [ [sg.Text('Send Image via NTP')],
            [sg.Text("Choose a file: "), sg.Input(key="-IN3-", change_submits=True), sg.FileBrowse(key="-INImage-", file_types=(("Image Files", "*.jpg")))] ]

# ----------- Create actual layout using Columns and a row of Buttons
layout = [  [sg.Text('Send via NTP')],
            [sg.Button('Message'), sg.Button('Text File'), sg.Button('Image File')],
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
            convert_text_to_ascii(values["-IN1-"])
        if layout == 2:
            read_text_from_file(values["-IN2-"])
        if layout == 3:
            read_image_from_file(values["-IN3-"])
            print(values["-IN3-"])
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
window.close()