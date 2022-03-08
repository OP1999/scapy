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

# # Window allowing the user to choose whether to send or receive a message with a server
# layout = [  [sg.Text("Input the message you would like to send to the server")],
#             [sg.Input()],
#             [sg.Text(size=(40,1), key='-OUTPUT-')],
#             [sg.Button('Send')]]

# window = sg.Window('Send Server Message', layout)
                                                
# event, value = window.read()
# sg.popup("Your message: ", value[0], "will be sent to the server")

# window.close()
# textToSend = value[0]

with open('NTPSampleText.txt') as f:
    readFile = f.readlines()
textToSend = readFile[0]

ascii_values = [ord(character) for character in textToSend]

cryptoKey = 40
ntpMessage = ""

def send_custom_packet(offset):
    # Sends a packet with the length of the message
    if(len(ascii_values) < 10):
        refTimeWithOffset = float128(str(datetime.datetime.timestamp(datetime.datetime.utcnow()))[:-3] + "00" + offset) + NTPMethods.date_diff
    else:
        refTimeWithOffset = float128(str(datetime.datetime.timestamp(datetime.datetime.utcnow()))[:-3] + "0" + offset) + NTPMethods.date_diff

    initialPacket = IP(dst=localIP)/UDP(sport=localPort, dport=destinationPort)/NTP(version=4, mode='client', ref=refTimeWithOffset)
    # initialPacket = IP(dst=localIP)/UDP(sport=localPort)/NTP(version=4, mode='client', ref=refTimeWithOffset)
    initialPacket.show()
    send(initialPacket)

# send_custom_packet(cryptoKey)
send_custom_packet(str(len(ascii_values)))

while(True):
    # Runs for the length of the message it is sending
    for i in range(len(textToSend)):
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
        ntpMessage += character
        # print(ntpMessage)

        time.sleep(1)
    
    if(len(ntpMessage) == len(textToSend)):
        print(ntpMessage)
        # Prints Message Received & Writes it to a text file then closes connection
        with open("NTPClientMessage.txt", "w") as text_file:
            print(f"{ntpMessage}", file=text_file)

        sg.popup("Message: ", value[0], "Successfully sent to the server")

    print(ntpMessage)
    time.sleep(5)   
    NTPClientSocket.close()