# Program to scan a subnet and pipe the results to nmap_out_1.csv
#
# written by Stuart Davis
#

import nmap
import csv

# Open the ldap_out.csv file, read-only, for taking the list of computer objects/hostnames for deploying agent
ADfile = open('ldap_out.csv','r')
# open the nmap_out.csv file which will contain the nmap results for the systems with ADMIN$ open from the list
nmapfile = open('nmap_out.csv','w')

# findTrgt function will take the subnet or list of hostnames and enumerate TCP/445 or the RPC port for ADMIN$ share access/open.
# It will take the results and write to the file nmap_out.csv

def findTrgt(subnet):
	nmapscan = nmap.PortScanner()
	nmapscan.scan(subnet, '445')
	trgtHosts = []
	for Hosts in nmapscan.all_hosts():
		if nmapscan[Hosts].has_tcp(445):
			state = nmapscan[Hosts]['tcp'][445]['state']
			if state == 'open':
				print '[+] Found open ADMIN$ on host: ' + Hosts
				nmapfile.write(Hosts+"\n")
				trgtHosts.append(Hosts)
	return trgtHosts

# open the ldap_out.csv file so we can take all the hostnames and pass them to the findTrgt() function
ADRead = csv.reader(ADfile, delimiter="\n")
for row in ADRead:
	hostname = str(row).replace('[','').replace(']','')
	print(hostname)
	#result = findTrgt(hostname)
	print(result)

# close the nmap file
nmapfile.close()
