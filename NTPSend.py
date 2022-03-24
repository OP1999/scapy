from numpy import float128
from scapy.all import *
import socket
import NTPMethods
import datetime
import os.path

clientIP = "127.0.0.1"
clientPort = 50005
serverIP = "127.0.0.1"
serverPort = 20005
bufferSize = 1024

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
    packet = IP(dst=clientIP)/UDP(sport=clientPort, dport=serverPort)/NTP(version=4, mode='client', ref=refTimeWithOffset)
    send(packet)

def get_ntp_packet(type, NTPSocket):
    bytesAddressPair = NTPSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]

    answer = NTPMethods.NTPPacket()
    answer = NTPMethods.unpack(answer, message, type)

def send_text_packet(int_values):
    global layout
    global ntpMessage
    ntpMessage = ""
    # Runs for the length of the message it is sending
    for i in range(len(int_values)):
        send_packet(get_message_value(int_values[i]))

        answer = get_ntp_packet(2, "NTPSocket")
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