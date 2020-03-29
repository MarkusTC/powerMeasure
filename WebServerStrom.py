#!/usr/bin/env python
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import os
import json
import time
import RPi.GPIO as GPIO
import threading

counter=0

#Rückgabe der Anzahl der Drehungen der Zählerscheibe
class respStrom(object):
    def __init__(self):
        self.bezei = 'gesamt'
        self.count=25

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
 
  # GET
  def do_GET(self):
        global counter
        # Send response status code
        self.send_response(200)
 
        parsed =  urlparse.urlparse(self.path)
        query =  urlparse.parse_qs(parsed.query)
        print(str(query))

        if "read" in query:          
          if query["read"][0]=="all":
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>Daten vom Stromzähler</title></head>","utf-8"))
            #self.wfile.write(bytes("<body><p>This is a test.</p>","utf-8"))
            ret=respStrom()
            ret.bezei="Impulse"
            ret.count=counter
            #Counter reseten
            counter=0
            s = json.dumps(ret.__dict__) 
            self.wfile.write(bytes(s,"utf-8"))
       
def display_standby(standby): #Display in Standby setzen
    if standby:
      PROCNAME = "vcgencmd display_power 1"
    else:
      PROCNAME = "vcgencmd display_power 0" 

    os.system(PROCNAME)

def count():
  print("es geht los")
  # Zählweise der Pins festlegen
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(7, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

  # Schleifenzähler
  global counter
  an=False
  # Endlosschleife
  while 1:
    # Eingang lesen
    if GPIO.input(7) == GPIO.HIGH and not an:
      # Wenn Eingang HIGH ist, Ausgabe im Terminal erzeugen
      counter = counter + 1
      an=True
      print ("Impuls " + str(counter))
      # Schleifenzähler erhöhen
      
    elif GPIO.input(7) == GPIO.LOW and an:
      #print ("aus")
      an=False
    time.sleep(0.1)  

def run():
  print('starting server...')
 
  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('192.168.178.45', 8080)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  
  # Start Webserver in an extra Thread
  thread = threading.Thread(None, httpd.serve_forever)
  thread.start()

#Haupt-Programm 
#global counter  
#counter=0
run()
print("next")
count()