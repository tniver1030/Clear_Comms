#TODO - run in background as taskbar icon
#TODO - make respond to web socket command
#TODO - Bot disconnect?

import http.client, urllib.parse
import time
from pynput.keyboard import Key, Listener
import socket
import wx
import wx.adv


TRAY_TOOLTIP = 'System Tray Demo'
TRAY_ICON = 'icon.png'

debug = False

directory = '/OBB'
host = 'fuckbis.ddns.net'
port = 42069
passcode = '6A41C4F91A9DE6E38938A91D2392F99D'

if debug:
    host = '127.0.0.1'
    port = 80
    

def keyPress(key):    
    if key == Key.ctrl_r:
        try:
            print('\nYou Entered {0}'.format( key))
            conn = http.client.HTTPConnection(host = host, port = port)
            params = urllib.parse.urlencode({'passcode': passcode})
            url = directory + '?' +  params
            conn.request('GET', url, body=None)
            response = conn.getresponse()
            print (response.status)
            conn.close()
        except Exception as e: print(e)

with Listener(on_press = keyPress) as listener:
 listener.join()
 
print('Stopping Keyboard Listener')

