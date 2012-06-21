#!/usr/bin/python
"""Copyright 2008 Orbitz WorldWide

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License."""

import sys
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

    while at > daybefore:
      lines = []

      values[0] += random.random() - 0.5
      values[1] += random.random() - 0.5
      values[2] += random.random() - 0.5

      lines.append("system%d.loadavg_1min %s %d" % (sysi, values[0],at))
      lines.append("system%d.loadavg_5min %s %d" % (sysi, values[1],at))
      lines.append("system%d.loadavg_15min %s %d" % (sysi, values[2],at))

      message = '\n'.join(lines) + '\n' #all lines must end in a newline
      print "sending message\n"
      print '-' * 80
      print message
      print

      sock.sendall(message)

      at -= 30
