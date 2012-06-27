#!/usr/bin/python
import time
import random
from socket import socket

CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 2003

sock = socket()
try:
  sock.connect( (CARBON_SERVER,CARBON_PORT) )
except:
  print "Couldn't connect to %(server)s on port %(port)d, is carbon-agent.py running?" % { 'server':CARBON_SERVER, 'port':CARBON_PORT }
  sys.exit(1)

while True:
  at = int(time.time())

  for user in xrange(1,500): # together - 500 * 2000 = 100000 per minute
   for i in xrange(1,2000):
    line = "user%d.system%d.half_timestamp %s %d" % (user, i, (at + (i * 10000) + (user * 10000)) ,at)

    message = line + '\n' #all lines must end in a newline
    
    sock.sendall(message)
    
    #print line
    time.sleep(0.0006)

