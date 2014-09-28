#/usr/bin/python
# Script to take user credentials details for deploying Agent MSI file
# created by Stuart Davis
#

#import Modules
import ConfigParser
import os
import time
import getpass
import base64
import ipaddr

def is_valid_ip_address(address, version=None):
#Check validity of address
#Return True if 'address' is a valid ipv4 or ipv6 address
# Validate version:
    if version:
        if not isinstance(version, int):
            raise TypeError, 'Version is not of type "int"'
            return False
        if not (version == 4 or version == 6):
            raise ValueError, 'IP version is set to an invalid number: %s' % version
            return False
    try:
        ipaddr.IPAddress(address.strip(),version)
    except ValueError:
        return False
    return True

def is_valid_ipv4_address(address):
#Check validity of address
#Return True if 'address' is a valid ipv4 address
    return is_valid_ip_address(address,4)


# check if there is a config.ini file already and notify the user
config = ConfigParser.ConfigParser()
config.read('config.ini')
return_v = config.read('config.ini')
if len(return_v) > 0:
	print "\n"
	print('config.ini file ALREADY EXISTS, overwriting!')
print """
+++++++++++++++++++++++++++++++++++++
+				    +
+ Enter Your Configuration Details  +
+				    +				    
+ Hit Ctrl+c to cancel the program  +
+++++++++++++++++++++++++++++++++++++
"""
print "Enter Domain Admin Username:"
user = raw_input()

print "Password will not be visible:"
passwordi = getpass.getpass()
password = base64.b64encode(passwordi)

print "Enter domain:"
domain = raw_input()

print "Enter AD IP:"
ad_ip = raw_input()

valid_ad_ip = is_valid_ipv4_address(ad_ip)

print "is the IP you entered valid: ",valid_ad_ip
if valid_ad_ip == False:
	print "Sorry, the script will not work with an incorrect IPV4 address, please restart script"
	print "The config still has the incorrect details"
else:
	print "Completed Successfully"

filestamp = time.strftime('%Y-%m-%d-%I:%M')

# uncomment the following if you want to troubleshoot the variables
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#print "\n"
#print "++ Details ++"
#print "User: %s" % (user)
#print "Password: %s" % (password)
#print "Domain Name: %s" % (domain)
#print "Domain AD Server IP: %s" % (ad_ip)
#print "File creation date: %s" % (filestamp)

# config = ConfigParser.ConfigParser()
# config.read('config.ini')
# return_v = config.read('config.ini')
# if len(return_v) > 0:
#        print('Please note that a config.ini file already exists')

if len(return_v) == 0:
	open('config.ini', 'wr')
	#raise ValueError, "Failed to open the file config.ini"
# Add the sections that ConfigParser expects
while not config.has_section('Credentials') == True:
	config.add_section('Credentials')
        config.add_section('Domain')
        config.add_section('Date')

config.set("Credentials", "User", "%s" % (user))
config.set("Credentials", "password", "%s" % (password))
config.set("Domain", "Name", "%s" % (domain))
config.set("Domain", "IP", "%s" % (ad_ip))
config.set("Date", "Created", "%s" % (filestamp))

with open('config.ini', 'w') as configfile:
	config.write(configfile)

