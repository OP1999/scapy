import os
import struct
import io
from numpy import float128
from scapy import sendrecv
from scapy.layers.inet import IP, UDP
from scapy.layers.ntp import NTP
import datetime
import docx
from PIL import Image

# These Values can be changed to users liking
serverIP = "127.0.0.1"
serverPort = 123
clientIP = "127.0.0.1"
clientPort = 1023
bufferSize = 1024

date_diff = (datetime.date(1970, 1, 1) - datetime.date(1900, 1, 1)).days * 24 * 3600

class NTPPacket:
    _FORMAT = "!B B b b 11I"
    def __init__(self, version_number=4, mode=3, transmit=float128):
        # Necessary of enter leap second (2 bits)
        self.leap_indicator = 0
        # Version of protocol (3 bits)
        self.version_number = version_number
        # Mode of sender (3 bits)
        self.mode = mode
        # The level of "layering" reading time (1 byte)
        self.stratum = 0
        # Interval between requests (1 byte)
        self.pool = 0
        # Precision (log2) (1 byte)
        self.precision = 0
        # Interval for the clock reach NTP server (4 bytes)
        self.root_delay = 0
        # Scatter the clock NTP-server (4 bytes)
        self.root_dispersion = 0
        # Indicator of clocks (4 bytes)
        self.ref_id = 0
        # Last update time on server (8 bytes)
        self.reference = 0
        # Time & Date of reference from server (8 bytes)
        self.referenceDate = datetime
        # Time of sending packet from local machine (8 bytes)
        self.originate = 0
        # Time & Date of reference from local machine (8 bytes)
        self.originateDate = datetime
        # Time of receipt on server (8 bytes)
        self.receive = 0
        # Time & Date of receipt on server (8 bytes)
        self.receiveDate = datetime
        # Time of sending answer from server (8 bytes)
        self.transmit = transmit
        # Time & Date of sending answer from server (8 bytes)
        self.transmitDate = datetime
        # Character sent from server (8 bytes)
        self.character = int

def get_fraction(number, precision):
    return int((number - int(number)) * 2 ** precision)

def unpack(self, data: bytes, type: int):
    unpacked_data = struct.unpack(NTPPacket._FORMAT, data)
    self.leap_indicator = unpacked_data[0] >> 6  # 2 bits
    self.version_number = unpacked_data[0] >> 3 & 0b111  # 3 bits
    self.mode = unpacked_data[0] & 0b111  # 3 bits
    self.stratum = unpacked_data[1]  # 1 byte
    self.pool = unpacked_data[2]  # 1 byte
    self.precision = unpacked_data[3]  # 1 byte
    # 2 bytes | 2 bytes
    self.root_delay = (unpacked_data[4] >> 16) + \
        (unpacked_data[4] & 0xFFFF) / 2 ** 16
     # 2 bytes | 2 bytes
    self.root_dispersion = (unpacked_data[5] >> 16) + \
        (unpacked_data[5] & 0xFFFF) / 2 ** 16 
    # 4 bytes
    self.ref_id = str((unpacked_data[6] >> 24) & 0xFF) + " " + \
        str((unpacked_data[6] >> 16) & 0xFF) + " " +  \
        str((unpacked_data[6] >> 8) & 0xFF) + " " +  \
        str(unpacked_data[6] & 0xFF)
    self.reference = unpacked_data[7] + unpacked_data[8] / 2 ** 32  # 8 bytes
    self.referenceDate = datetime.datetime.fromtimestamp(self.reference) - datetime.timedelta(days=25567)
    self.originate = unpacked_data[9] + unpacked_data[10] / 2 ** 32  # 8 bytes
    self.originateDate = datetime.datetime.fromtimestamp(self.originate) - datetime.timedelta(days=25567)
    self.receive = unpacked_data[11] + unpacked_data[12] / 2 ** 32  # 8 bytes
    self.receiveDate = datetime.datetime.fromtimestamp(self.receive) - datetime.timedelta(days=25567)
    self.transmit = unpacked_data[13] + unpacked_data[14] / 2 ** 32  # 8 bytes
    self.transmitDate = datetime.datetime.fromtimestamp(self.transmit) - datetime.timedelta(days=25567)
    # Gets the character of the message
    # Server Response from Ref and takes last three digits
    if(type == 1):
        self.character = int((f"{str(round(unpacked_data[8] / 2 ** 32, 6))[:8]:0<8}")[-3:])
    # Client Response from Rec and takes last three digits
    elif(type == 2):
        self.character = int((f"{str(round(unpacked_data[12] / 2 ** 32, 6))[:8]:0<8}")[-3:])
    # Takes entire 6 digits of fraction to get Message Length
    # Server Response from Ref
    elif(type == 3):
        self.character = (int(round(unpacked_data[8] / 2 ** 32, 6) * 1000000))
    # Client Response from Rec
    elif(type == 4):
        self.character = (int(round(unpacked_data[12] / 2 ** 32, 6) * 1000000))

    return self

# Returns the value of the character from above (usually less than 255)
def get_mess_val(self):
    digit = self.character
    return digit

# Returns the character as a letter
def get_mess_char(self):
    letter = chr(self.character)
    return letter

# Returns all the NTP timestamps
def get_all_ntp_times(self):
    referenceDate = self.referenceDate
    originateDate = self.originateDate
    receiveDate = self.receiveDate
    transmitDate = self.transmitDate
    return [referenceDate, originateDate, receiveDate, transmitDate]

# Returns the edited timestamps
def get_spec_ntp_times(self):
    referenceDate = self.referenceDate
    receiveDate = self.receiveDate
    return [referenceDate, receiveDate]

# Returns all the packet info
def to_display(self):
    return "Leap indicator: {0.leap_indicator}\n" \
            "Version number: {0.version_number}\n" \
            "Mode: {0.mode}\n" \
            "Stratum: {0.stratum}\n" \
            "Pool: {0.pool}\n" \
            "Precision: {0.precision}\n" \
            "Root delay: {0.root_delay}\n" \
            "Root dispersion: {0.root_dispersion}\n" \
            "Ref id: {0.ref_id}\n" \
            "Reference: {0.reference}\n" \
            "Reference Date: {0.referenceDate}\n" \
            "Originate: {0.originate}\n" \
            "Originate Date: {0.originateDate}\n" \
            "Receive: {0.receive}\n" \
            "Receive Date: {0.receiveDate}\n" \
            "Transmit: {0.transmit}\n"\
            "Transmit Date: {0.transmitDate}\n" \
            .format(self)

# Returns the legnth of the message - used for initial packet
def get_message_length_time(value):
    # Formats Current Time to Set string value - Upto 6 digits
    currentTime = f"{str(datetime.datetime.timestamp(datetime.datetime.now()) + date_diff)[:17][:-6]:0<17}"
    timeWithValue = float128(currentTime[:-len(str(value))] + str(value)) 

    return timeWithValue

# Edits the timestamp to include the byte information
def get_message_value_time(value):
    # Formats Current Time to Set string value - 3 digits - max of 255
    currentTime = f"{str(datetime.datetime.timestamp(datetime.datetime.now()) + date_diff)[:17]:0<17}"
    if(value < 10):
        timeWithValue = float128(currentTime[:-3] + "00" + str(value)) 
    elif(value >=  10 and value < 100):
        timeWithValue = float128(currentTime[:-3] + "0" + str(value)) 
    else:
        timeWithValue = float128(currentTime[:-3] + str(value)) 

    return timeWithValue

# Reading From Text / Doc Files
def read_text_from_file(fileName, destIp, locPort, destPort, NTPType):
    if(os.path.splitext(fileName)[1] == '.docx'):
        return send_text(getTextFromDoc(fileName), destIp, locPort, destPort, NTPType)
    elif(os.path.splitext(fileName)[1] == '.txt'):
        return send_text(getTextFromTxt(fileName), destIp, locPort, destPort, NTPType)
    else:
        return 6

# Reading From png / jpg Files
def read_image_from_file(fileName, destIp, locPort, destPort, NTPType): 
    if(os.path.splitext(fileName)[1] == '.png'):
        with open(fileName, "rb") as image:
            image_values = image.read()
            send_packet(get_message_value_time(2), destIp, locPort, destPort, NTPType)
            send_packet(get_message_length_time(len(image_values)), destIp, locPort, destPort, NTPType)
            return image_values
    elif(os.path.splitext(fileName)[1] == '.jpg'):
        with open(fileName, "rb") as image:
            image_values = image.read()
            send_packet(get_message_value_time(2), destIp, locPort, destPort, NTPType)
            send_packet(get_message_length_time(len(image_values)), destIp, locPort, destPort, NTPType)
            return image_values
    else:
        return 6

# Reading From zip File
def read_zip_from_file(fileName, destIp, locPort, destPort, NTPType):
    if(os.path.splitext(fileName)[1] == '.zip'):
        with open(fileName, "rb") as zip:
            zip_values = zip.read()
            send_packet(get_message_value_time(3), destIp, locPort, destPort, NTPType)
            send_packet(get_message_length_time(len(zip_values)), destIp, locPort, destPort, NTPType)
            return zip_values
    else:
        return 6

# Reads the text from doc file
def getTextFromDoc(fileName):
    doc = docx.Document(fileName)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

# Reads the text from txt file
def getTextFromTxt(fileName):
    with open(fileName) as f:
            readFile = f.readlines()
    return readFile[0]

# Converts text to ascii values
def convert_text_to_ascii(textToSend):
    ascii_values = [ord(character) for character in textToSend]
    
    return ascii_values

# Sending NTP TextPacket
def send_text(textToSend, destIp, locPort, destPort, NTPType):
    send_packet(get_message_value_time(1), destIp, locPort, destPort, NTPType)
    ascii_values = convert_text_to_ascii(textToSend)
    send_packet(get_message_length_time(len(ascii_values)), destIp, locPort, destPort, NTPType)
    
    return ascii_values

# Sending edited NTP Packet as either client or server
def send_packet(timeWithOffset, destIp, locPort, destPort, NTPType):
    if(NTPType == 'client'):
        packet = IP(dst=destIp)/UDP(sport=locPort, dport=destPort)/NTP(version=4, mode=NTPType, ref=timeWithOffset)
    elif(NTPType == 'server'):
        packet = IP(dst=destIp)/UDP(sport=locPort, dport=destPort)/NTP(version=4, mode=NTPType, recv=timeWithOffset)

    sendrecv.send(packet)

# Sending a default NTP Packet as either client or server
def send_default_packet(destIp, locPort, destPort, NTPType):
    if(NTPType == 'client'):
        packet = IP(dst=destIp)/UDP(sport=locPort, dport=destPort)/NTP(version=4, mode=NTPType)
    elif(NTPType == 'server'):
        packet = IP(dst=destIp)/UDP(sport=locPort, dport=destPort)/NTP(version=4, mode=NTPType)

    sendrecv.send(packet)

# Listens for NTP Packet sent to socket
def get_ntp_packet(NTPSocket, NTPType):
    bytesAddressPair = NTPSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]

    answer = NTPPacket()
    answer = unpack(answer, message, NTPType)

    return answer

# Method for Listening for NTP packet with the message length
def get_message_len_method(NTPSocket, NTPtype):
    if(NTPtype == 'server'):
        answer = get_ntp_packet(NTPSocket, 3)
    elif(NTPtype == 'client'):
        answer = get_ntp_packet(NTPSocket, 4)
    arrayLength = get_mess_val(answer)

    return arrayLength

# Sets whether to be run in client or server mode
def get_ntp_type(NTPtype):
    if(NTPtype == 'server'):
        return 1
    elif(NTPtype == 'client'):
        return 2

# Receives packets, identifies packet type and length
def receive_packet(NTPSocket, destIP, locPort, destPort, NTPtype):
    ntpMode = 1
    if(NTPtype == 'client'):   
        print("NTP Client Listening Active")
    elif(NTPtype == 'server'):   
        print("NTP Server Listening Active")
    while(ntpMode == 1):
        answer = get_ntp_packet(NTPSocket, get_ntp_type(NTPtype))

        # Gets File Type of message and Length
        messageType = get_mess_val(answer)
        # send_default_packet(destIP, locPort, destPort, NTPtype)
        messageLength = get_message_len_method(NTPSocket, NTPtype)
        # send_default_packet(destIP, locPort, destPort, NTPtype)

        if(messageType == 1):
            response = receive_text_packet(NTPSocket, messageLength, destIP, locPort, destPort, NTPtype)
        elif(messageType == 2):
            response = receive_byte_packet(NTPSocket, messageLength, messageType, destIP, locPort, destPort, NTPtype)
        elif(messageType == 3):
            response = receive_byte_packet(NTPSocket, messageLength, messageType, destIP, locPort, destPort, NTPtype)
        
        ntpMode = response [1]
    
    return response

# Receives the text packets for txt and doc files
def receive_text_packet(NTPSocket, messageLength, destIP, locPort, destPort, NTPtype):
    ntpMessage = ""
    # Runs for the length of the message it is receiving
    for i in range(messageLength):
        answer = get_ntp_packet(NTPSocket, get_ntp_type(NTPtype))

        # # for returning a default ntp packet response when a packet is received
        # send_default_packet(destIP, locPort, destPort, NTPtype)

        # # for printing the ntp packet received
        # ntpResponse = NTPMethods.to_display(answer)
        # print(ntpResponse)

        character = get_mess_char(answer)
        ntpMessage += character
    
    # Sends the length of the message received for verification
    send_packet(get_message_length_time(len(ntpMessage)), destIP, locPort, destPort, NTPtype)

    if(len(ntpMessage) == messageLength):
        # Writes NTP Message received to a text file
        with open("NTPCliServMessage.txt", "w") as text_file:
            print(f"{ntpMessage}", file=text_file)

    ntpMode = 0

    if(len(ntpMessage) > 30):
        ntpMessage = "Text"

    return(ntpMessage, ntpMode)

# Receives the byte packets for image and zip files
def receive_byte_packet(NTPSocket, byteLength, byteType, destIP, locPort, destPort, NTPtype):
    ntpArray = []
    ntpMessage = ""
    # Runs for the length of the message it is receiving
    for i in range(byteLength):
        answer = get_ntp_packet(NTPSocket, get_ntp_type(NTPtype))

        # # for returning a default ntp packet response when a packet is received
        # send_default_packet(destIP, locPort, destPort, NTPtype)
        
        # # for printing the ntp packet received
        # ntpResponse = NTPMethods.to_display(answer)
        # print(ntpResponse)
        
        character = get_mess_val(answer)
        ntpArray.append(character)

    # Sends the length of the message received for verification
    send_packet(get_message_length_time(len(ntpArray)), destIP, locPort, destPort, NTPtype)
    
    if(byteType == 2):
        if(len(ntpArray) == byteLength):
            # Writes NTP Message to an image file
            byteArray = bytearray(ntpArray)
            
            image = Image.open(io.BytesIO(byteArray))
            image.save("NTPCliServImg.jpg")

        ntpMessage = "Image"
        
    elif(byteType == 3):
        if(len(ntpArray) == byteLength):
            # Writes NTP Message to a zip file
            byteArray = bytearray(ntpArray)

            with open("NTPCliServZip.zip", 'wb') as zip_file:
                zip_file.write(byteArray)

        ntpMessage = "Zip"   

    ntpMode = 0

    return(ntpMessage, ntpMode)

# send the text packet
def send_text_packet(NTPSocket, int_values, destIP, locPort, destPort, NTPtype):
    # Runs for the length of the message it is sending
    for i in range(len(int_values)):
        send_packet(get_message_value_time(int_values[i]), destIP, locPort, destPort, NTPtype)

    # Gets the length of the recived message
    ntpMessage = str(get_message_len_method(NTPSocket, NTPtype))

    # reset layout
    layout = 5
    ntpMode = 3

    return(ntpMessage, layout, ntpMode)

# send the byte packet
def send_byte_packet(NTPSocket, int_values, destIP, locPort, destPort, NTPtype):
    # Runs for the length of the message it is sending
    for i in range(len(int_values)):
        send_packet(get_message_value_time(int_values[i]), destIP, locPort, destPort, NTPtype)

    # Gets the length of the recived message
    ntpMessage = str(get_message_len_method(NTPSocket, NTPtype))

    # reset layout
    layout = 5
    ntpMode = 3

    return(ntpMessage, layout, ntpMode)