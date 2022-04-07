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

window = sg.Window('Client', GUI.centredLayout, size=(480,220))

while True:
    event, values = window.read()
    if event in (None, '-BTNExit-'):
        NTPSocket.close()
        break
    GUI.gui_window(window, event, values, NTPSocket, destinationIP, localPort, destinationPort, NTPType)
window.close()