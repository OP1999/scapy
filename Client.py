from scapy.all import *
import socket
import NTPMethods
import GUI
import PySimpleGUI as sg

localIP = NTPMethods.clientIP
localPort = NTPMethods.clientPort
destinationIP = NTPMethods.serverIP
destinationPort = NTPMethods.serverPort
NTPType = 'client'

# Create a UDP socket at Client side
NTPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
NTPSocket.bind((localIP, localPort))
print("NTP Client Up")

global layout
global ntpMode
global ntpMessage

window = sg.Window('Client', GUI.winLayout, size=(500,300), element_justification='c')

layout = 1  # The currently visible layout
ntpMessage = ""
ntpMode = 0

while True:
    event, values = window.read()
    if event in (None, '-BTNExit-'):
        NTPSocket.close()
        break
    GUI.gui_window(window, event, values, NTPSocket, destinationIP, localPort, destinationPort, NTPType)
window.close()