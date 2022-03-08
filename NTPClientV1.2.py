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

# Window allowing the user to choose whether to send or receive a message with a server
layout = [  [sg.Text("Input the message you would like to send to the server")],
            [sg.Input()],
            [sg.Text(size=(40,1), key='-OUTPUT-')],
            [sg.Button('Send')]]

window = sg.Window('Send Server Message', layout)
                                                
event, value = window.read()
sg.popup("Your message: ", value[0], "will be sent to the server")

window.close()

# textToSend = "hi"
textToSend = value[0]
ntpMessage = ""
ntpReceived = ""

ascii_values = [ord(character) for character in textToSend]
# print(ascii_values)

# Sends a packet with the length of the message
if(len(ascii_values) < 10):
    refTimeWithLength = float128(str(datetime.datetime.timestamp(datetime.datetime.utcnow()))[:-3] + "00" + str(len(ascii_values))) + NTPMethods.date_diff
else:
    refTimeWithLength = float128(str(datetime.datetime.timestamp(datetime.datetime.utcnow()))[:-3] + "0" + str(len(ascii_values))) + NTPMethods.date_diff

initialPacket = IP(dst=localIP)/UDP(sport=localPort, dport=destinationPort)/NTP(version=4, mode='client', ref=refTimeWithLength)
# initialPacket = IP(dst=localIP)/UDP(sport=localPort)/NTP(version=4, mode='client', ref=refTimeWithLength)
initialPacket.show()
send(initialPacket)

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

        # serverIP  = "Server IP Address:{}".format(address)
        # print(serverIP)

        answer = NTPMethods.NTPPacket()
        answer = NTPMethods.unpack(answer, message, 2)
        ntpResponse = NTPMethods.to_display(answer)
        character = NTPMethods.get_message(answer)

        print(ntpResponse)
        ntpReceived += character
        
        # # Should Print letter 'R' if message successfully received
        # print(character)
        
        # # Prints Message Received
        # ntpMessage += character
        # print(ntpMessage)

        time.sleep(1)
    
    if(len(ntpReceived) == len(textToSend)):
        # Prints Message Received & Writes it to a text file the closes connection
        with open("NTPClientMessage.txt", "w") as text_file:
            print(f"{ntpMessage}", file=text_file)

        sg.popup("Message: ", value[0], "Successfully sent to the server")

    time.sleep(10)   
    NTPClientSocket.close()