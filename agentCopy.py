# agentCopy
# Script to copy the Agent MSI file to a list of hosts obtained from a file ldap_out.csv. 
# The ldap_out file has results returned from the ldapconnect.py script
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

# open the output from the ldapconnect script. This will contain the computer
# hostnames that we will be copying the MSI file to for installation.
openfile = open('nmap_out.csv','r')
# open the file using csv.reader to parse the values into a list
# smbcopy expects the target in the format [domain/][username[:password]@]<address>
reader = csv.reader(openfile, delimiter='\n')
for row in reader:
	new_row = str(row).replace('[','').replace(']','')
	print "deploying to:",new_row
	subprocess.call(['smbcopy.py %s/%s:%s@%s ../AgentSetup_11.3.12_universal.msi'%(domain,domain_user,domain_user_pass,new_row)],stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
	subprocess.call(['smbcopy.py %s/%s:%s@%s ../conf.xml'%(domain,domain_user,domain_user_pass,new_row)],stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
	subprocess.call(['smbcopy.py %s/%s:%s@%s ../Magent_install_11_3_12.bat'%(domain,domain_user,domain_user_pass,new_row)],stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
	
	#subprocess.call(['smbcopy.py mandiant:mandiant@%s ../AgentSetup_11.3.12_universal.msi'%new_row],stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
   	#subprocess.call(['smbcopy.py mandiant:mandiant@%s ../conf.xml'%new_row],stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
   	#subprocess.call(['smbcopy.py mandiant:mandiant@%s ../Magent_install_11_3_12.bat'%new_row],stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
	#subprocess.call(['smbcopy.py mandiant:mandiant@%s ../AgentSetup_11.3.12_universal.msi'%new_row],stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
   	#subprocess.call(['smbcopy.py mandiant:mandiant@%s ../conf.xml'%new_row],stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
   	#subprocess.call(['smbcopy.py mandiant:mandiant@%s ../Magent_install_11_3_12.bat'%new_row],stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
	#subprocess.call(['smbcopy.py mandiant:mandiant@%s ../AgentSetup_11.3.12_universal.msi'%new_row],stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
   	#subprocess.call(['smbcopy.py mandiant:mandiant@%s ../conf.xml'%new_row],stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
   	#subprocess.call(['smbcopy.py mandiant:mandiant@%s ../Magent_install_11_3_12.bat'%new_row],stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
	#subprocess.call(['smbcopy.py mandiant:mandiant@%s ../AgentSetup_11.3.12_universal.msi'%new_row],stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
   	#subprocess.call(['smbcopy.py mandiant:mandiant@%s ../conf.xml'%new_row],stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
   	#subprocess.call(['smbcopy.py mandiant:mandiant@%s ../Magent_install_11_3_12.bat'%new_row],stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
