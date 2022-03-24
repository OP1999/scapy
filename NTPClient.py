from numpy import float128
from scapy.all import *
import socket
import NTPMethods
import datetime
import PySimpleGUI as sg
import os.path

localIP = "127.0.0.1"
localPort = 50005
destinationIP = "127.0.0.1"
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
        send_packet(get_message_value(1))
        convert_text_to_ascii(textToSend)    
    elif(os.path.splitext(fileName)[1] == '.txt'):
        textToSend = NTPMethods.getTextFromTxt(fileName)
        send_packet(get_message_value(1))
        convert_text_to_ascii(textToSend)
    else:
        layout = 5

def read_image_from_file(fileName): 
    global layout
    if(os.path.splitext(fileName)[1] == '.png'):
        with open(fileName, "rb") as image:
            image_values = image.read()
            send_packet(get_message_value(2))
            send_packet(get_message_length(len(image_values)))
            send_byte_packet(image_values)
    elif(os.path.splitext(fileName)[1] == '.jpg'):
        with open(fileName, "rb") as image:
            image_values = image.read()
            send_packet(get_message_value(2))
            send_packet(get_message_length(len(image_values)))
            send_byte_packet(image_values)
    else:
        layout = 5

def read_zip_from_file(fileName): 
    global layout
    if(os.path.splitext(fileName)[1] == '.zip'):
        with open(fileName, "rb") as zip:
            zip_values = zip.read()
            send_packet(get_message_value(3))
            send_packet(get_message_length(len(zip_values)))
            send_byte_packet(zip_values)
    else:
        layout = 5

def convert_text_to_ascii(textToSend):
    ascii_values = [ord(character) for character in textToSend]
    send_packet(get_message_length(len(ascii_values)))
    send_text_packet(ascii_values)

def get_message_value(value):
    # Formats Current Time to Set string value - 3 digits - max of 255
    currentTime = f"{str(datetime.datetime.timestamp(datetime.datetime.utcnow()) + NTPMethods.date_diff)[:17]:0<17}"
    if(value < 10):
        refTimeWithValue = float128(currentTime[:-3] + "00" + str(value)) 
    elif(value >=  10 and value < 100):
        refTimeWithValue = float128(currentTime[:-3] + "0" + str(value)) 
    else:
        refTimeWithValue = float128(currentTime[:-3] + str(value)) 

    return refTimeWithValue

def get_message_length(value):
    # Formats Current Time to Set string value - Upto 6 digits
    currentTime = f"{str(datetime.datetime.timestamp(datetime.datetime.utcnow()) + NTPMethods.date_diff)[:17][:-6]:0<17}"
    refTimeWithValue = float128(currentTime[:-len(str(value))] + str(value)) 

    return refTimeWithValue

def send_packet(refTimeWithOffset):
    packet = IP(dst=localIP)/UDP(sport=localPort, dport=destinationPort)/NTP(version=4, mode='client', ref=refTimeWithOffset)
    send(packet)

def send_text_packet(int_values):
    global layout
    global ntpMessage
    ntpMessage = ""
    # Runs for the length of the message it is sending
    for i in range(len(int_values)):
        send_packet(get_message_value(int_values[i]))

        bytesAddressPair = NTPClientSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        
        # address = bytesAddressPair[1]
        # serverIP = "Server IP Address:{}".format(address)
        # print(serverIP)

        answer = NTPMethods.NTPPacket()
        answer = NTPMethods.unpack(answer, message, 2)
        # ntpResponse = NTPMethods.to_display(answer)
        character = NTPMethods.get_message_char(answer)

        # print(ntpResponse)
        
        # Should Print letter 'R' if message successfully received
        ntpMessage += character
    
    if(len(ntpMessage) == len(int_values)):
        print(ntpMessage)
        # Prints Message Received & Writes it to a text file then closes connection
        with open("NTPClientMessage.txt", "w") as text_file:
            print(f"{ntpMessage}", file=text_file)
    
    layout = 0

def send_byte_packet(int_values):
    global layout
    global ntpMessage
    ntpMessage = ""
    # Runs for the length of the message it is sending
    for i in range(len(int_values)):
        send_packet(get_message_value(int_values[i]))

    ntpMessage = "Bytes Sent"

    layout = 0

# ----------- Create the 4 layouts this Window will display -----------
layoutSuccSent = [  [sg.Text(key="-ErrorMess-")],
                    [sg.Text(key="-NTPText-")]    ]

layout1 = [ [sg.Text("Input the message you would like to send to the server")],
            [sg.Input(key="-INMes-")]    ]

layout2 = [ [sg.Text('Send Text File via NTP')],
            [sg.Text("Choose a file: "), sg.Input(key="-INTxt-", change_submits=True), sg.FileBrowse(key="-INFBTxt-", file_types=(("Text Files", "*.txt")))] ]
            
layout3 = [ [sg.Text('Send Image via NTP')],
            [sg.Text("Choose a file: "), sg.Input(key="-INImg-", change_submits=True), sg.FileBrowse(key="-INFBImage-", file_types=(("Image Files", "*.jpg")))] ]

layout4 = [ [sg.Text('Send Zip via NTP')],
            [sg.Text("Choose a file: "), sg.Input(key="-INZip-", change_submits=True), sg.FileBrowse(key="-INFBZip-", file_types=(("Zip Files", "*.zip")))] ]

# ----------- Create actual layout using Columns and a row of Buttons
winLayout = [  [sg.Text('Send via NTP')],
            [sg.Button('Message'), sg.Button('Text File'), sg.Button('Image File'), sg.Button('Zip File')],
            [sg.Column(layout1, key='-COL1-'), sg.Column(layout2, visible=False, key='-COL2-'), sg.Column(layout3, visible=False, key='-COL3-'), sg.Column(layout4, visible=False, key='-COL4-')],
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
            send_packet(get_message_value(1))
            convert_text_to_ascii(values["-INMes-"])
        if layout == 2:
            read_text_from_file(values["-INTxt-"])
        if layout == 3:
            read_image_from_file(values["-INImg-"])
        if layout == 4:
            read_zip_from_file(values["-INZip-"])
    if event == 'Message':
        layout = 1
        window[f'-COLSuccSent-'].update(visible=False)
        window[f'-COL2-'].update(visible=False)
        window[f'-COL3-'].update(visible=False)
        window[f'-COL4-'].update(visible=False)
        window[f'-BTNSend-'].update(visible=True)
        window[f'-COL1-'].update(visible=True)  
    elif event == 'Text File':
        layout = 2
        window[f'-COLSuccSent-'].update(visible=False)
        window[f'-COL1-'].update(visible=False)
        window[f'-COL3-'].update(visible=False)
        window[f'-COL4-'].update(visible=False)
        window[f'-BTNSend-'].update(visible=True)
        window[f'-COL2-'].update(visible=True)
    elif event == 'Image File':
        layout = 3
        window[f'-COLSuccSent-'].update(visible=False)
        window[f'-COL1-'].update(visible=False)
        window[f'-COL2-'].update(visible=False)
        window[f'-COL4-'].update(visible=False)
        window[f'-BTNSend-'].update(visible=True)
        window[f'-COL3-'].update(visible=True)
    elif event == 'Zip File':
        layout = 4
        window[f'-COLSuccSent-'].update(visible=False)
        window[f'-COL1-'].update(visible=False)
        window[f'-COL2-'].update(visible=False)
        window[f'-COL3-'].update(visible=False)
        window[f'-BTNSend-'].update(visible=True)
        window[f'-COL4-'].update(visible=True)
    if layout == 0:
        window[f'-ErrorMess-'].update("Client successfully Sent a Message")
        window[f'-NTPText-'].update('Message Received: ' + ntpMessage)
        window[f'-COLSuccSent-'].update(visible=True)
        window[f'-BTNSend-'].update(visible=False)
        window[f'-COL1-'].update(visible=False)
        window[f'-COL2-'].update(visible=False)
        window[f'-COL3-'].update(visible=False)
        window[f'-COL4-'].update(visible=False)
    if layout == 5:
        window[f'-ErrorMess-'].update("Unsuccessful Sending File")
        window[f'-NTPText-'].update('Wrong File Type - Please choose again')
        window[f'-COLSuccSent-'].update(visible=True)
        window[f'-BTNSend-'].update(visible=False)
        window[f'-COL1-'].update(visible=False)
        window[f'-COL2-'].update(visible=False)
        window[f'-COL3-'].update(visible=False)
        window[f'-COL4-'].update(visible=False)
window.close()