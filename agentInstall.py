# This script will run a remote WMI call against the list of computers in the AD_out.csv file, that have 
# had the Agent install MSI file copied across via the agentCopy.py script
#
# created by Stuart Davis

import subprocess
import os
import csv
import ConfigParser
import base64

# open the config.ini file to parse the configuration details.
conf = ConfigParser.ConfigParser()
conf.read('config.ini')
# read the configuration details from config.ini file
domain = conf.get('Domain', 'name', 0)
domain_user = conf.get('Credentials', 'user', 0)
domain_user_pass_encr = conf.get('Credentials', 'password', 0)
domain_user_pass = base64.b64decode(domain_user_pass_encr)

# hostnames that we will be copying the MSI file to for installation.
openfile = open('nmap_out.csv','r')
# open the file using csv.reader to put the values into a list
reader = csv.reader(openfile, delimiter='\n')

for row in reader:
   new_row = str(row).replace('[','').replace(']','')
   subproc = subprocess.call(['psexec.py %s/%s:%s@%s "C:\\Windows\\Magent_install_11_3_12.bat" >> agent_install_psexec_log.txt'%(domain,domain_user,domain_user_pass,new_row)],stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
   print "Subprocess response [0] is success, [1] failure. Returned value is:", subproc
   print "the Row value is:", row
   print "the nmap output is:", new_row
