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

# # Window allowing the user to choose whether to send or receive a message with a client
# layout = [  [sg.Text("Input the message you would like to send to the client")],
#             [sg.Input()],
#             [sg.Text(size=(40,1), key='-OUTPUT-')],
#             [sg.Button('Send')]]

# window = sg.Window('Send Client Message', layout)
                                                
# event, value = window.read()
# sg.popup("Your message: '", value[0], "' will be sent to the client")

textToSend = "hello client"
# textToSend = value[0]
ntpMessage = ""

ascii_values = [ord(character) for character in textToSend]

while(True): 
    bytesAddressPair = NTPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]

    answer = NTPMethods.NTPPacket()
    answer = NTPMethods.unpack(answer, message, 1)
    messageLength = NTPMethods.get_message_length(answer)
    print('Message Length: ' + str(messageLength))
    
    # Runs for the length of the message it is receiving / sending
    for i in range(messageLength):
        bytesAddressPair = NTPServerSocket.recvfrom(bufferSize)
        
        # # Replies 'R' to show letter is received
        # recTimeWithMessage = float128(str(datetime.datetime.timestamp(datetime.datetime.utcnow()))[:-3] + "082") + NTPMethods.date_diff
        
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]

        # clientIP = "Client IP Address:{}".format(address)   
        # print(clientIP)

        answer = NTPMethods.NTPPacket()
        answer = NTPMethods.unpack(answer, message, 1)
        ntpResponse = NTPMethods.to_display(answer)
        character = NTPMethods.get_message(answer)
        try:
            if(ascii_values[i] < 100):
                recTimeWithMessage = float128(str(datetime.datetime.timestamp(datetime.datetime.utcnow()))[:-3] + "0" + str(ascii_values[i])) + NTPMethods.date_diff
            else :
                recTimeWithMessage = float128(str(datetime.datetime.timestamp(datetime.datetime.utcnow()))[:-3] + str(ascii_values[i])) + NTPMethods.date_diff
        except:
            recTimeWithMessage = float128(str(datetime.datetime.timestamp(datetime.datetime.utcnow()))[:-3] + "032") + NTPMethods.date_diff
            
        returnPacket = IP(dst=address[0])/UDP(sport=localPort,dport=address[1])/NTP(version=4, mode='server', recv=recTimeWithMessage)
        send(returnPacket)

        print(ntpResponse)

        # Prints Message Received
        ntpMessage += character
        # print(ntpMessage)
    
    if(len(ntpMessage) == messageLength):
        # Prints Message Received & Writes it to a text file then closes connection
        with open("NTPServerMessage.txt", "w") as text_file:
            print(f"{ntpMessage}", file=text_file)
    
        sg.popup("Message:", ntpMessage, "Successfully received from client")
    
    print(ntpMessage)
    time.sleep(5)   
    NTPServerSocket.close()