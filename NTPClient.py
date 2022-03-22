from numpy import float128
from scapy.all import *
import socket
import NTPMethods
import datetime
import PySimpleGUI as sg
import os.path

localIP = "127.0.0.1"
localPort = 50005
destinationPort = 20005
bufferSize = 1024

# Create a UDP socket at Client side
NTPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
NTPClientSocket.bind((localIP, localPort))
print("NTP Client Up")

# cryptoKey = 40
global layout
global ntpMessage

def read_text_from_file(fileName):
    global layout
    if(os.path.splitext(fileName)[1] == '.docx'):
        textToSend = NTPMethods.getTextFromDoc(fileName)
        send_message_type('1')
        convert_text_to_ascii(textToSend)    
    elif(os.path.splitext(fileName)[1] == '.txt'):
        textToSend = NTPMethods.getTextFromTxt(fileName)
        send_message_type('1')
        convert_text_to_ascii(textToSend)
    else:
        layout = 4

def read_image_from_file(fileName): 
    global layout
    if(os.path.splitext(fileName)[1] == '.png'):
        with open(fileName, "rb") as image:
            image_values = image.read()
            send_message_type('2')
            send_message_length(len(image_values))
            send_image_packet(image_values)
    elif(os.path.splitext(fileName)[1] == '.jpg'):
        with open(fileName, "rb") as image:
            image_values = image.read()
            send_message_type('2')
            send_message_length(len(image_values))
            send_image_packet(image_values)
    else:
        layout = 4

def convert_text_to_ascii(textToSend):
    ascii_values = [ord(character) for character in textToSend]
    send_message_length(len(ascii_values))
    send_client_packet(ascii_values)

def send_message_type(fileType):
    # Sends a packet with the type of file type of the message - 1, 2 or 3
    refTimeWithTypeOffset = float128(str(datetime.datetime.timestamp(datetime.datetime.utcnow()))[:-3] + "00" + fileType) + NTPMethods.date_diff

    print(refTimeWithTypeOffset)
    send_packet_length_type_offset(refTimeWithTypeOffset)

def send_message_length(length):
    # Sends a packet with the length of the message
    if(length < 10):
        refTimeWithLengthOffset = float128(str(datetime.datetime.timestamp(datetime.datetime.utcnow()))[:-3] + "00" + str(length)) + NTPMethods.date_diff
    elif(length >=  10 and length < 100):
        refTimeWithLengthOffset = float128(str(datetime.datetime.timestamp(datetime.datetime.utcnow()))[:-3] + "0" + str(length)) + NTPMethods.date_diff
    else:
        refTimeWithLengthOffset = float128(str(datetime.datetime.timestamp(datetime.datetime.utcnow()))[:-len(str(length))] + str(length)) + NTPMethods.date_diff

    print(refTimeWithLengthOffset)
    send_packet_length_type_offset(refTimeWithLengthOffset)

def send_packet_length_type_offset(refTimeWithOffset):
    initialPacket = IP(dst=localIP)/UDP(sport=localPort, dport=destinationPort)/NTP(version=4, mode='client', ref=refTimeWithOffset)
    # initialPacket = IP(dst=localIP)/UDP(sport=localPort)/NTP(version=4, mode='client', ref=refTimeWithOffset)
    send(initialPacket)

def send_client_packet(int_values):
    global layout
    global ntpMessage
    ntpMessage = ""
    # Runs for the length of the message it is sending
    for i in range(len(int_values)):
        if(int_values[i] < 10):
            refTimeWithMessage = float128(str(datetime.datetime.timestamp(datetime.datetime.utcnow()))[:-3] + "00" + str(int_values[i])) + NTPMethods.date_diff
        elif(int_values[i] >=  10 and int_values[i] < 100):
            refTimeWithMessage = float128(str(datetime.datetime.timestamp(datetime.datetime.utcnow()))[:-3] + "0" + str(int_values[i])) + NTPMethods.date_diff
        else:
            # refTimeWithMessage = float128(str(datetime.datetime.timestamp(datetime.datetime.utcnow()))[:-(len(str(int_values[i])))] + str(int_values[i])) + NTPMethods.date_diff
            refTimeWithMessage = float128(str(datetime.datetime.timestamp(datetime.datetime.utcnow()))[:-3] + str(int_values[i])) + NTPMethods.date_diff

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

        # print(ntpResponse)
        
        # Should Print letter 'R' if message successfully received
        ntpMessage += character

        # time.sleep(1)
    
    if(len(ntpMessage) == len(int_values)):
        print(ntpMessage)
        # Prints Message Received & Writes it to a text file then closes connection
        with open("NTPClientMessage.txt", "w") as text_file:
            print(f"{ntpMessage}", file=text_file)
    
    layout = 0

def send_image_packet(int_values):
    global layout
    global ntpMessage
    ntpMessage = ""
    # Runs for the length of the message it is sending
    for i in range(len(int_values)):
        if(int_values[i] < 10):
            refTimeWithMessage = float128(str(datetime.datetime.timestamp(datetime.datetime.utcnow()))[:-3] + "00" + str(int_values[i])) + NTPMethods.date_diff
        elif(int_values[i] >=  10 and int_values[i] < 100):
            refTimeWithMessage = float128(str(datetime.datetime.timestamp(datetime.datetime.utcnow()))[:-3] + "0" + str(int_values[i])) + NTPMethods.date_diff
        else:
            # refTimeWithMessage = float128(str(datetime.datetime.timestamp(datetime.datetime.utcnow()))[:-(len(str(int_values[i])))] + str(int_values[i])) + NTPMethods.date_diff
            refTimeWithMessage = float128(str(datetime.datetime.timestamp(datetime.datetime.utcnow()))[:-3] + str(int_values[i])) + NTPMethods.date_diff

        clientPacket = IP(dst=localIP)/UDP(sport=localPort, dport=destinationPort)/NTP(version=4, mode='client', ref=refTimeWithMessage)
        # clientPacket = IP(dst=localIP)/UDP(sport=localPort)/NTP(version=4, mode='client', ref=refTimeWithMessage)
        send(clientPacket)

    layout = 0

# ----------- Create the 4 layouts this Window will display -----------
layoutSuccSent = [  [sg.Text(key="-ErrorMess-")],
                    [sg.Text(key="-NTPText-")]    ]

layout1 = [ [sg.Text("Input the message you would like to send to the server")],
            [sg.Input(key="-IN1-")]    ]

layout2 = [ [sg.Text('Send Text File via NTP')],
            [sg.Text("Choose a file: "), sg.Input(key="-IN2-", change_submits=True), sg.FileBrowse(key="-INFile-", file_types=(("Text Files", "*.txt")))] ]
            
layout3 = [ [sg.Text('Send Image via NTP')],
            [sg.Text("Choose a file: "), sg.Input(key="-IN3-", change_submits=True), sg.FileBrowse(key="-INImage-", file_types=(("Image Files", "*.jpg")))] ]

# ----------- Create actual layout using Columns and a row of Buttons
winLayout = [  [sg.Text('Send via NTP')],
            [sg.Button('Message'), sg.Button('Text File'), sg.Button('Image File')],
            [sg.Column(layout1, key='-COL1-'), sg.Column(layout2, visible=False, key='-COL2-'), sg.Column(layout3, visible=False, key='-COL3-')],
            [sg.Column(layoutSuccSent, key='-COLSuccSent-', visible=False)],
            [sg.Button('Send', key='-BTNSend-'), sg.Button('Exit', key='-BTNExit-')]    ]

window = sg.Window('Send Data via NTP', winLayout, size=(500,250), element_justification='c')

layout = 1  # The currently visible layout
while True:
    event, values = window.read()
    # print(event, values)
    if event in (None, '-BTNExit-'):
        NTPClientSocket.close()
        break
    if event == "-BTNSend-":
        if layout == 1:
            send_message_type('1')
            convert_text_to_ascii(values["-IN1-"])
        if layout == 2:
            read_text_from_file(values["-IN2-"])
        if layout == 3:
            read_image_from_file(values["-IN3-"])
            print(values["-IN3-"])
    if event == 'Message':
        layout = 1
        window[f'-COLSuccSent-'].update(visible=False)
        window[f'-COL2-'].update(visible=False)
        window[f'-COL3-'].update(visible=False)
        window[f'-BTNSend-'].update(visible=True)
        window[f'-COL1-'].update(visible=True)  
    elif event == 'Text File':
        layout = 2
        window[f'-COLSuccSent-'].update(visible=False)
        window[f'-COL1-'].update(visible=False)
        window[f'-COL3-'].update(visible=False)
        window[f'-BTNSend-'].update(visible=True)
        window[f'-COL2-'].update(visible=True)
    elif event == 'Image File':
        layout = 3
        window[f'-COLSuccSent-'].update(visible=False)
        window[f'-COL1-'].update(visible=False)
        window[f'-COL2-'].update(visible=False)
        window[f'-BTNSend-'].update(visible=True)
        window[f'-COL3-'].update(visible=True)
    if layout == 0:
        window[f'-ErrorMess-'].update("Client successfully Sent a Message")
        window[f'-NTPText-'].update('Message Received: ' + ntpMessage)
        window[f'-COLSuccSent-'].update(visible=True)
        window[f'-BTNSend-'].update(visible=False)
        window[f'-COL1-'].update(visible=False)
        window[f'-COL2-'].update(visible=False)
        window[f'-COL3-'].update(visible=False)
    if layout == 4:
        window[f'-ErrorMess-'].update("Unsuccessful Sending File")
        window[f'-NTPText-'].update('Wrong File Type - Please choose again')
        window[f'-COLSuccSent-'].update(visible=True)
        window[f'-BTNSend-'].update(visible=False)
        window[f'-COL1-'].update(visible=False)
        window[f'-COL2-'].update(visible=False)
        window[f'-COL3-'].update(visible=False)
window.close()