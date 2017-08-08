#!/usr/bin/python
import sys
import socket
import re
import thread
import time
import datetime
import os

bufsiz = 2048

LOG_PRIMASK = 0x07
PRIMASK = [
    "emerg",
    "alert",
    "crit",
    "err",
    "warning",
    "notice",
    "info",
    "debug"
]

FACILITYMASK = [
    "kern",
    "user",
    "mail",
    "daemon",
    "auth",
    "syslog",
    "lpr",
    "news",
    "uucp",
    "cron",
    "authpriv",
    "ftp",
    "ntp",
    "security",
    "console",
    "mark",
    "local0",
    "local1",
    "local2",
    "local3",
    "local4",
    "local5",
    "local6",
    "local7"
]


def byte2string(byte):
    '''
    Convert syslog classification byte to facility and priority.
    The first 5 bits are the facility
    The last 3 bits are the priority

    See pg9 http://www.syslog.cc/ietf/drafts/draft-ietf-syslog-protocol-23.txt
    '''
    try:
        facility = FACILITYMASK[byte >> 3]
        priority = PRIMASK[byte & LOG_PRIMASK]
        return "%s.%s" % (facility, priority)

    except Exception as err:
        print "Unexpected facility or priority: %s.%s" % (facility, priority)
        print err
        return "unknown.unknown"


class SyslogListener(object):
    def datagramReceived(self, data):
        """strip priority tag"""
        if data[2] == ">":
            pri = byte2string(int(data[1]))
            msg = data[3:]
        elif data[3] == ">":
            pri = byte2string(int(data[1:3]))
            msg = data[4:]
        else:
            pri = None
            msg = data
        msg = msg.strip()
        print "%s:%s" % (pri, msg)

    def listen(self):
        try:
            os.remove('/dev/log')
        except:
            pass
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
            sock.bind("/dev/log")
            self.sock = sock

        except:
            print "Socket error: (%s) %s " % (sys.exc_info()[1][0],
                                              sys.exc_info()[1][1])
            sys.exit(1)

        while 1:
            try:
                data, addr = sock.recvfrom(bufsiz)
                self.datagramReceived(data)
            except KeyboardInterrupt:
                self.shutdown()
                return
            except socket.error:
                pass

    def shutdown(self):
        try:
            self.sock.close()
        except:
            pass

        try:
            os.remove('/dev/log')
        except:
            pass


if __name__ == '__main__':
    # disable output buffer
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    lst = SyslogListener()
    lst.listen()
