from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import configparser

configFile = 'config.ini'
config = configparser.ConfigParser()
config.read(configFile)

DEBUG = config.getboolean('Default','debug')
hostName = config.get('WebServer','hostName')
serverPort = config.getint('WebServer','port')
buffer_directory = config.get('WebServer','buffer_directory')
enabled = config.getboolean('WebServer','enabled')
passcode = config.get('WebServer','passcode')
code_required = config.getboolean('WebServer','code_required')

global verified 
verified = False

if(DEBUG):
    print("Setting Debug Variables")
    hostName = "127.0.0.1"
    serverPort = 80
    code_required = False


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))  
        
        config.read(configFile)
        enabled = config.getboolean('WebServer','enabled')
        path = self.path
        
        if DEBUG:        
            print(path)
            
        
        if not code_required:
            verified = True
        else:
            verified = False
        
        code = path.split("=")
        if (code[1] == passcode):#Get first parameter for passcode
            verified = True
            print('PASSCODE ACCEPTED')
        else:
            print('WRONG PASSCODE')
        
        path = path.split("?") #Get directory
        path = path[0]
        
        if(path != '/favicon.ico') & enabled & verified:
            print('Writing :', path, ' to :', buffer_directory)
            publication_buffer = open(buffer_directory, 'w')    
            publication_buffer.write(path)
            publication_buffer.close()
            verified = False
        elif not enabled:
            print('Not enabled!')

if not DEBUG:          
    time.sleep(10)
    #Needed for boot sequencing on linux?

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:    
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")