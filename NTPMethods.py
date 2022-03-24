from scapy.all import *
import datetime
import numpy as np
import docx

# Package Struct
# IP(version=4,ihl= None,tos= 0x0,len= None,id= 1,flags= ,frag= 0,ttl= 64,proto= "udp",chksum= None,src= "127.0.0.1",dst= "127.0.0.1"
# /UDP(sport='ntp',dport=20005,len=none,chksum=none)
# /NTP(leap=1,version=4,mode='client',stratum=3,poll=10,precision=0.1,delay=0.1,dispersion=0.1,id=127.0.0.1,ref=5,orig=--,recv=1,sent=--)

base_time = datetime.datetime(1900, 1, 1)
date_diff = (datetime.date(1970, 1, 1) - datetime.date(1900, 1, 1)).days * 24 * 3600
# FORMAT_DIFF = (datetime.date(1970, 1, 1) - datetime.date(1900, 1, 1))

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
    self.referenceDate = datetime.datetime.fromtimestamp(self.reference) - timedelta(days=25567)
    self.originate = unpacked_data[9] + unpacked_data[10] / 2 ** 32  # 8 bytes
    self.originateDate = datetime.datetime.fromtimestamp(self.originate) - timedelta(days=25567)
    self.receive = unpacked_data[11] + unpacked_data[12] / 2 ** 32  # 8 bytes
    self.receiveDate = datetime.datetime.fromtimestamp(self.receive) - timedelta(days=25567)
    self.transmit = unpacked_data[13] + unpacked_data[14] / 2 ** 32  # 8 bytes
    self.transmitDate = datetime.datetime.fromtimestamp(self.transmit) - timedelta(days=25567)
    # Gets the character of the message
    # Server and takes last three digits
    if(type == 1):
        self.character = int((f"{str(round(unpacked_data[8] / 2 ** 32, 6))[:8]:0<8}")[-3:])
    # Client and takes last three digits
    elif(type == 2):
        self.character = int((f"{str(round(unpacked_data[12] / 2 ** 32, 6))[:8]:0<8}")[-3:])
    # Message Length
    elif(type == 4):
        self.character = (int(round(unpacked_data[8] / 2 ** 32, 6) * 1000000))

    return self

def get_message(self):
    letter = chr(self.character)
    return letter

def get_byte_digit(self):
    digit = self.character
    return digit

def get_message_type(self):
    length = self.character
    return length

def get_message_length(self):
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

def extract_origin_timestamp(ntp_packet):
    encoded_origin_timestamp = ntp_packet[24:32]

    seconds, fraction = struct.unpack("!II", encoded_origin_timestamp)
    offset = datetime.timedelta(seconds=seconds + fraction / 2**32)
    return base_time + offset

def extract_transmit_timestamp(ntp_packet):
    encoded_transmit_timestamp = ntp_packet[40:48]

    seconds, fraction = struct.unpack("!II", encoded_transmit_timestamp)
    offset = datetime.timedelta(seconds=seconds + fraction / 2**32)
    return base_time + offset

def extract_receive_timestamp(ntp_packet):
    encoded_receive_timestamp = ntp_packet[32:40]

    seconds, fraction = struct.unpack("!II", encoded_receive_timestamp)
    offset = datetime.timedelta(seconds=seconds + fraction / 2**32)
    return base_time + offset

# origin_timestamp = NTPMethods.extract_origin_timestamp(message)
# print("Origin clock read (in UTC):", origin_timestamp)
# transmit_timestamp = NTPMethods.extract_transmit_timestamp(message)
# print("Transmit clock read (in UTC):", transmit_timestamp)

# Sending a reply to client
# NTPServerSocket.sendto(ntpBytesToSend, address)

# send(IP(dst='127.0.0.1')/UDP(sport=50005,dport=20005)/NTP(version=4))