import socket
import NTPMethods
import GUI
import PySimpleGUI as sg

localIP = NTPMethods.serverIP
localPort = NTPMethods.serverPort
destinationIP = NTPMethods.clientIP
destinationPort = NTPMethods.clientPort
NTPType = 'server'

# Create a UDP socket at server side
NTPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
NTPSocket.bind((localIP, localPort))
print("NTP Server Up")

window = sg.Window('Server', GUI.winLayout, size=(500,300), element_justification='c')

while True:
    event, values = window.read()
    if event in (None, '-BTNExit-'):
        NTPSocket.close()
        break
    GUI.gui_window(window, event, values, NTPSocket, destinationIP, localPort, destinationPort, NTPType)
window.close()