#
# Code to retrieve Computer objects from MS Active Directory
# Take objects list and parse a RegeX to pull the list of distinguishedNames
# Written by Stuart Davis
#

import ldap
import sys 
from ldap.controls import SimplePagedResultsControl
import os
import re
import ConfigParser
import base64

# Define my variables to help with the Size Limit Exceeded issue in MSAD
COOKIE = ''
PAGE_SIZE = 1000
CRITICALITY = True
results = []
first_pass = True

# open the config.ini file to parse the configuration details.
import ConfigParser
conf = ConfigParser.ConfigParser()
conf.read('config.ini')
# read the configuration details from config.ini file
domain = conf.get('Domain', 'name', 0)
domain_user = conf.get('Credentials', 'user', 0)
domain_user_pass_encr = conf.get('Credentials', 'password', 0)
domain_user_pass = base64.b64decode(domain_user_pass_encr)

try:
    	# Open the initial connection to the LDAP server
	l = ldap.initialize("ldap://%s:389"%domain)
    	# When searching from the domain level MS AD returns referrals (search continuations) for some objects to 
    	# indicate to the client where to look for these objects. Client-chasing of referrals is a broken concept 
    	# since LDAPv3 does not specify which credentials to use when chasing the referral. Windows clients are supposed 
    	# to simply use their Windows credentials but this does not work in general when chasing referrals received from 
    	# and pointing to arbitrary LDAP servers. Therefore per default libldap automatically chases the referrals internally 
    	# with an anonymous access which fails with MS AD. So best thing is to switch this behaviour off :)
    	l.set_option(ldap.OPT_REFERRALS, 0)
    	# Bind/authenticate with a user with apropriate rights to add objects
    	l.simple_bind_s("%s@%s"%(domain_user,domain), "%s"%domain_user_pass)
	#l.simple_bind_s("Administrator@mandiant.edu", "mandiant123!")
    	## searching doesn't require a bind in LDAP V3.  If you're using LDAP v2, set the next line appropriately
    	## and do a bind as shown in the above example.
    	# you can also set this to ldap.VERSION2 if you're using a v2 directory
    	# you should  set the next option to ldap.VERSION2 if you're using a v2 directory
    	l.protocol_version = ldap.VERSION3

except ldap.LDAPError, e:
	print e

# require the values in this format - baseDN = "DC=mandiant, DC=edu"
splitVal = domain.split('.')
baseDN = "DC=%s, DC=%s"%(splitVal[0],splitVal[1])
#baseDN = "DC=mandiant, DC=edu"
print "baseDN is:",baseDN
searchScope = ldap.SCOPE_SUBTREE

## retrieve all attributes - again adjust to your needs - see documentation for more options
retrieveAttributes = ['dNSHostName', 'distinguishedName'] 
# searchFilter. Options can include CN=, etc
searchFilter = "objectClass=computer"
pg_ctrl = SimplePagedResultsControl(CRITICALITY, PAGE_SIZE, COOKIE)
while first_pass or pg_ctrl.cookie:
    first_pass = False
    try:
        msgid = l.search_ext(baseDN, searchScope, searchFilter, retrieveAttributes, serverctrls=[pg_ctrl])
    except ldap.LDAPError, e:
            print e

    result_type, data, msgid, serverctrls = l.result3(msgid)
    # print "data is: ", data
    # print "serverctrls value is: ", serverctrls
    # pg_ctrl.cookie = serverctrls[0].cookie
    if len(serverctrls) > 0: pg_ctrl.cookie = serverctrls[0].cookie
    results += [i[0] for i in data]

# convert results to a string as re.findall will not accept a List
results_str = str(results)
# Active Directory
# The regular expression to pull only the distinguishedName attribute from the LDAP query is:
AD_reg = "'CN=([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9]),"
# open our csv file that was dumped from our LDAP computer objects lookup
# read the contents of the file
# use a findall function to parse through file searching for content based on the regex
output = re.findall(AD_reg, results_str ,flags=0)
# print the results
#open file and export results 
file = open('ldap_out.csv','w')
#Loop all computer hostnames and deploy Agent MSI
for names in output:
	file.write(names+'\n')
	print names
# unbind the connection from Active Directory
l.unbind_s()
