from numpy import float128
from scapy.all import *
import datetime
import numpy as np
import docx

# Package Struct
# IP(version=4,ihl= None,tos= 0x0,len= None,id= 1,flags= ,frag= 0,ttl= 64,proto= "udp",chksum= None,src= "127.0.0.1",dst= "127.0.0.1"
# /UDP(sport='ntp',dport=20005,len=none,chksum=none)
# /NTP(leap=1,version=4,mode='client',stratum=3,poll=10,precision=0.1,delay=0.1,dispersion=0.1,id=127.0.0.1,ref=5,orig=--,recv=1,sent=--)

serverIP = "127.0.0.1"
serverPort = 20005
clientIP = "127.0.0.1"
clientPort = 50005
bufferSize = 1024

base_time = datetime.datetime(1900, 1, 1)
date_diff = (datetime.date(1970, 1, 1) - datetime.date(1900, 1, 1)).days * 24 * 3600

ntpMode = 10
ntpMessage = ""
ntpArray = []

class NTPPacket:
    _FORMAT = "!B B b b 11I"
    def __init__(self, version_number=4, mode=3, transmit=np.float64):
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
    # Client Response from Ori and takes last three digits
    elif(type == 2):
        self.character = int((f"{str(round(unpacked_data[12] / 2 ** 32, 6))[:8]:0<8}")[-3:])
    # Message Length
    elif(type == 4):
        self.character = (int(round(unpacked_data[8] / 2 ** 32, 6) * 1000000))

    return self

def get_byte_digit(self):
    digit = self.character
    return digit

def get_mess_char(self):
    letter = chr(self.character)
    return letter

def get_mess_type(self):
    length = self.character
    return length

def get_mess_length(self):
    length = self.character
    return length

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

def get_message_length(value):
    # Formats Current Time to Set string value - Upto 6 digits
    currentTime = f"{str(datetime.datetime.timestamp(datetime.datetime.utcnow()) + date_diff)[:17][:-6]:0<17}"
    refTimeWithValue = float128(currentTime[:-len(str(value))] + str(value)) 

    return refTimeWithValue

def get_message_value(value):
    # Formats Current Time to Set string value - 3 digits - max of 255
    currentTime = f"{str(datetime.datetime.timestamp(datetime.datetime.utcnow()) + date_diff)[:17]:0<17}"
    if(value < 10):
        refTimeWithValue = float128(currentTime[:-3] + "00" + str(value)) 
    elif(value >=  10 and value < 100):
        refTimeWithValue = float128(currentTime[:-3] + "0" + str(value)) 
    else:
        refTimeWithValue = float128(currentTime[:-3] + str(value)) 

    return refTimeWithValue

# Reading From Files
def read_text_from_file(fileName, destIp, locPort, destPort, mode):
    global layout
    if(os.path.splitext(fileName)[1] == '.docx'):
        return send_text(getTextFromDoc(fileName), destIp, locPort, destPort, mode)
    elif(os.path.splitext(fileName)[1] == '.txt'):
        return send_text(getTextFromTxt(fileName), destIp, locPort, destPort, mode)
    else:
        return 6

def read_image_from_file(fileName, destIp, locPort, destPort, mode): 
    if(os.path.splitext(fileName)[1] == '.png'):
        with open(fileName, "rb") as image:
            image_values = image.read()
            send_packet(get_message_value(2), destIp, locPort, destPort, mode)
            send_packet(get_message_length(len(image_values)), destIp, locPort, destPort, mode)
            return image_values
    elif(os.path.splitext(fileName)[1] == '.jpg'):
        with open(fileName, "rb") as image:
            image_values = image.read()
            send_packet(get_message_value(2), destIp, locPort, destPort, mode)
            send_packet(get_message_length(len(image_values)), destIp, locPort, destPort, mode)
            return image_values
    else:
        return 6

def read_zip_from_file(fileName, destIp, locPort, destPort, mode):
    if(os.path.splitext(fileName)[1] == '.zip'):
        with open(fileName, "rb") as zip:
            zip_values = zip.read()
            print(zip_values)
            send_packet(get_message_value(3), destIp, locPort, destPort, mode)
            send_packet(get_message_length(len(zip_values)), destIp, locPort, destPort, mode)
            return zip_values
    else:
        return 6

def getTextFromDoc(fileName):
    doc = docx.Document(fileName)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

def getTextFromTxt(fileName):
    with open(fileName) as f:
            readFile = f.readlines()
    return readFile[0]

def convert_text_to_ascii(textToSend):
    ascii_values = [ord(character) for character in textToSend]
    
    return ascii_values

# Sending NTP Packet
def send_text(textToSend, destIp, locPort, destPort, mode):
    send_packet(get_message_value(1), destIp, locPort, destPort, mode)
    ascii_values = convert_text_to_ascii(textToSend)
    send_packet(get_message_length(len(ascii_values)), destIp, locPort, destPort, mode)
    
    return ascii_values

def send_packet(refTimeWithOffset, destIp, locPort, destPort, mode):
    packet = IP(dst=destIp)/UDP(sport=locPort, dport=destPort)/NTP(version=4, mode=mode, ref=refTimeWithOffset)
    send(packet)

def get_ntp_packet(NTPSocket, type):
    bytesAddressPair = NTPSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]

    answer = NTPPacket()
    answer = unpack(answer, message, type)

    return answer

def get_message_len_method(NTPServer):
    answer = get_ntp_packet(NTPServer, 4)
    arrayLength = get_mess_length(answer)

    return arrayLength

def receive_message_length_method(NTPSocket):
    bytesAddressPair = NTPSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]

    answer = NTPPacket()
    answer = unpack(answer, message, 2)

    return get_mess_length(answer)