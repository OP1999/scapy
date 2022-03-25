from numpy import float128
from scapy.all import *
import socket
import NTPMethods
import PySimpleGUI as sg
import io
from PIL import Image

localIP = NTPMethods.serverIP
localPort = NTPMethods.serverPort
destinationIP = NTPMethods.clientIP
destinationPort = NTPMethods.clientPort

# Create a UDP socket at Server side
NTPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
NTPServerSocket.bind((localIP, localPort))
print("NTP Server Up")

global ntpMode
global ntpMessage
global ntpArray

ntpMessage = ""
ntpArray = []

def receive_client_packet():
    global ntpMode
    while(ntpMode == 1): 
        print("NTP Server Listening Active")
        answer = get_ntp_packet(1)

        messageType = NTPMethods.get_mess_type(answer)
        arrayLength = get_message_len()

        if(messageType == 1):
            receive_text_packet(arrayLength)
        elif(messageType == 2):
            receive_byte_packet(arrayLength, messageType)
        elif(messageType == 3):
            receive_byte_packet(arrayLength, messageType)
        
        ntpMode = 0 

def get_ntp_packet(type):
    bytesAddressPair = NTPServerSocket.recvfrom(NTPMethods.bufferSize)
    message = bytesAddressPair[0]

    answer = NTPMethods.NTPPacket()
    answer = NTPMethods.unpack(answer, message, type)

    return answer

def get_message_len():
    answer = get_ntp_packet(4)
    arrayLength = NTPMethods.get_mess_length(answer)

    return arrayLength

def receive_text_packet(messageLength):
    global ntpMessage
    ntpMessage = ""
    # Runs for the length of the message it is receiving
    for i in range(messageLength):
        answer = get_ntp_packet(1)
        # ntpResponse = NTPMethods.to_display(answer)
        character = NTPMethods.get_mess_char(answer)

        # print(ntpResponse)
        ntpMessage += character

    send_received_mess_length(len(ntpMessage))
    
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
            # Writes NTP Message to an image file
            byteArray = bytearray(ntpArray)
            
            image = Image.open(io.BytesIO(byteArray))
            image.save("NTPServerImg.jpg")

        ntpMessage = "Image"
    elif(type == 3):
        if(len(ntpArray) == byteLength):
            # Writes NTP Message to a zip file
            byteArray = bytearray(ntpArray)

            with open("NTPServerZip.zip", 'wb') as zip_file:
                zip_file.write(byteArray)

        ntpMessage = "Zip"
    
    send_received_mess_length(len(ntpArray))

def send_received_mess_length(messageLength):
    # Sends NTPPacket with size of the message length received
    recTimeWithMessage = NTPMethods.get_message_value(messageLength)
    
    returnPacket = IP(dst=destinationIP)/UDP(sport=localPort,dport=destinationPort)/NTP(version=4, mode='server', recv=recTimeWithMessage)
    send(returnPacket)

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
winLayout = [   [sg.Text('Server')],
            [sg.Button('Receive Mode'), sg.Button('Send Mode')],
            [sg.Column(layoutReceive, key='-COLReceive-', visible=False)],
            [sg.Column(layoutButton, key='-COLBtn-', visible=False)],
            [sg.Column(layoutSuccReceive, key='-COLSuccReceive-', visible=False)],
            [sg.Column(layoutMes, visible=False, key='-COLMes-'), sg.Column(layoutTxt, visible=False, key='-COLTxt-'), sg.Column(layoutImg, visible=False, key='-COLImg-'), sg.Column(layoutZip, visible=False, key='-COLZip-')],
            [sg.Column(layoutSuccSent, key='-COLSuccSent-', visible=False)],
            [sg.Button('Send', key='-BTNSend-', visible=False)], 
            [sg.Button('Exit', key='-BTNExit-')]    ]
window = sg.Window('Send / Receive Data via NTP', winLayout, size=(500,300), element_justification='c')

layout = 0
while True:
    event, values = window.read()
    if event in (None, '-BTNExit-'):
        NTPServerSocket.close()
        break
    # if event == "-BTNSend-":
        # if layout == 1:
        #     send_packet(get_message_value(1))
        #     convert_text_to_ascii(values["-INMes-"])
        # if layout == 2:
        #     read_text_from_file(values["-INTxt-"])
        # if layout == 3:
        #     read_image_from_file(values["-INImg-"])
        # if layout == 4:
        #     read_zip_from_file(values["-INZip-"])
    if event == 'Receive Mode':
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
        receive_client_packet() 
        window.refresh()
    elif event == 'Send Mode':
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
        window[f'-NTPRecText-'].update('Message Received: ' + ntpMessage)
        window[f'-COLReceive-'].update(visible=False)
        window[f'-COLSuccReceive-'].update(visible=True)
        window.bring_to_front()
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
window.close()