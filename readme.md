# Comnet
An TCP-based Commercial Botnet written in Python

### Current Version: v1.0 | [Changelog](updates.md)

## About Comnet
Comnet is a commercial botnet platform built in Python for the Linux OS.
It was designed to host a CNC server that only accepts connections from
authorized clients (eliminating illicit use of the software). Comnet is
capable of mass checking LAN IP services, scanning services for status
updates, broadband (server-load) balancing, and many more!

## Install/Requirements
To install and use Comnet, you'll need a Linux VPS with Python 2.7-3.x
installed. You then can install the requirements by running:
```
$ sudo -H pip install -r core/requirements.txt
$ python core/test.py
[*] Checking requirements...
[*] Checking configuration...
[+] Comnet's requirements have been met. You may now use the software!
```
Once you've reached this point, you may now start your Comnet server:
```
$ nano core/config.json # modify server configuration.
$ python server/comnet.py
...
```

## Disclaimer
Code samples are provided for educational purposes. Adequate defenses can only be built by researching attack techniques available to malicious actors. Using this code against target systems without prior permission is illegal in most jurisdictions. The authors are not liable for any damages from misuse of this information or code.

## Authors
 * Willy Fox ([@BlackVikingPro](https://github.com/BlackVikingPro))
 * [@Kar00t](https://github.com/Kar00t)
