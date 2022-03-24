from numpy import float128
from scapy.all import *
import socket
import datetime
import NTPMethods
import io
from PIL import Image

serverIP = "127.0.0.1"
serverPort = 20005
clientIP = "127.0.0.1"
clientPort = 50005
bufferSize = 1024

global ntpMode
global ntpMessage
global ntpArray

ntpMessage = ""
ntpArray = []

def get_ntp_packet(type, NTPServer):
    bytesAddressPair = NTPServer.recvfrom(bufferSize)
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
        answer = get_ntp_packet(1)
        # ntpResponse = NTPMethods.to_display(answer)
        character = NTPMethods.get_message_char(answer)

        # Replies 'R' to show letter is received
        recTimeWithMessage = float128(str(datetime.datetime.timestamp(datetime.datetime.utcnow()))[:-3] + "082") + NTPMethods.date_diff
        
        # returnPacket = IP(dst=address[0])/UDP(sport=serverPort,dport=address[1])/NTP(version=4, mode='server', recv=recTimeWithMessage)
        returnPacket = IP(dst=clientIP)/UDP(sport=serverPort,dport=clientPort)/NTP(version=4, mode='server', recv=recTimeWithMessage)
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