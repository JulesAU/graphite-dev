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

for sysi in xrange(1,5000):
    at = int( time.time() )
    daybefore = at - 24*60*60

    values = [0,0,0]
    
    lines = []

    while at > daybefore:
      values[0] += random.random() - 0.5
      values[1] += random.random() - 0.5
      values[2] += random.random() - 0.5

      lines.append("system%d.loadavg_1min %s %d" % (sysi, values[0],at))
      lines.append("system%d.loadavg_5min %s %d" % (sysi, values[1],at))
      lines.append("system%d.loadavg_15min %s %d" % (sysi, values[2],at))

      at -= 30

    message = '\n'.join(lines) + '\n' #all lines must end in a newline
    sock.sendall(message)

    print sysi
