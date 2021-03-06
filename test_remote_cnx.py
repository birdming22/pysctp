#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 
# Copyright (C) 2009 Philippe Langlois - all rights reserved
#
# Test with sctp_test from lksctp:
# sctp_test -H 127.0.0.1 -P 10000 -l
#
# Test with sctpscan from P1 Security / Philippe Langlois:
# sctpscan -d
# (see http://www.p1sec.com/corp/research/tools/sctpscan/ )
#
# (Works only with Python >= 2.3 because of OptionParser usage)
import _sctp
import sctp
from sctp import *
import time

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-H", "--host", dest="server",
                  help="connect to HOST", action = "store",  metavar="HOST", default="10.37.129.140")
# parser.add_option("-f", "--file", dest="filename",
#                   help="write report to FILE", metavar="FILE")
parser.add_option("-P", "--port", dest="tcpport",
                  help="connect to PORT", action = "store",  metavar="PORT", type="int", default=10000)
#
parser.add_option("-p", "--localport", dest="localport",
                  help="connect from local PORT", action = "store",  metavar="PORT", type="int", default=0)
parser.add_option("-q", "--quiet",
                  action="store_false", dest="verbose", default=True,
                  help="don't print status messages to stdout")

(options, args) = parser.parse_args()

# client = "127.0.0.1"
# server = "10.37.129.140" 
server = options.server
# tcpport = 10000
tcpport = options.tcpport

if _sctp.getconstant("IPPROTO_SCTP") != 132:
	raise "getconstant failed"
tcp = sctpsocket_tcp(socket.AF_INET)

saddr = (server, tcpport)
 
print "TCP ", saddr, " ----------------------------------------------"

tcp.initparams.max_instreams = 3
tcp.initparams.num_ostreams = 3

tcp.events.clear()
tcp.events.data_io = 1

if options.localport != 0:
   # tcp.bindx([("", options.localport)])
   print "Binding..."
   tcp.bind(("", options.localport))

tcp.connect(saddr)

tcp.sctp_send("ABCDEF: TEST SUCCEEDED (test_local_cnx.py (C) 2009 Philippe Langlois)\n\l")
while 1:
   fromaddr, flags, msgret, notif = tcp.sctp_recv(1000)
   print "	Msg arrived, flag %d" % flags

   if flags & FLAG_NOTIFICATION:
      raise "We did not subscribe to receive notifications!"
   # else:
   print "%s" % msgret

tcp.close()
