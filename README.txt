++++++++++++++++++++++++++++++++++++++++++++++++++
+    Documentation v0.1								                            
+    Information related to deployment scripts				            
+    FireEye Agent Remotedeploy Tool					                    
+    by Stuart Davis								                              
++++++++++++++++++++++++++++++++++++++++++++++++++

Pre-requisites
++++++++++++++
Requires Impacket and ipaddr. 
To work correctly, the agent remotedeploy tools require to have impacket 0.9.13-dev installed on the the Linux server that the scripts will be run from. http://corelabs.coresecurity.com/index.php?module=Wiki&action=view&type=tool&name=Impacket
in addition you will require http://code.google.com/p/ipaddr-py/ ipaddr python module installed.

Requires Python V <=2.7.3 

Installation
++++++++++++
firstly, install the impacket package by runing the setup.py script. To install the remote deployment scripts, simply copy the enterConfig, ldapconnect, nmap_enum, agentCopy and agentInstall python files into any working directory. Copy the Magent_install_11_2_12.bat, agent install MSI file and the conf.xml into a directory below the scripts, e.g. if the scripts are in /home/JohnS/Agent/Deploy, then put the agent MSI and other files in the /home/JohnS/Agent directory. 

Script Descriptions
+++++++++++++++++
The following section will describe briefly the function of the python scripts.
1. enterConfig.py: take user input to create a 'config.ini' file. This will be used by all scripts for configuration details
2. ldapconnect.py: connect to the MS Active Directory and will pull all computer objects and will output to a file 'ldap_out.csv'
3. nmap_enum.py:	parses the ldap_out.csv file and will resolve each entry to an IP and connect to each IP's RPC service and confirm if IPC$ share is available. output to a file 'nmap_out.csv'
5. agentCopy.py: parses the nmap_out.csv file and will connect to each IP and copy 3 files (agent MSI, conf.xml and install batch file). Uses credentials from config.ini
6. agentInstall.py: will remotely execute the install batch script copied to each system. Batch file will determine if FireEyeAgent is running, if not, it will install the agent.

Operation
++++++++++
During the use of the scripts, the following sequence can be used- First, run the enterConfig script ($ python enterConfig.py) and enter the deployment details including user auth details. Run the ldapconnect script ($ python ldapconnect.py) to connect to Active Directory to pull a list of the computer objects within a domain. The domain specified while running enterConfig.py will capture the domain in a file 'config.ini'. Once the ldapconnect script is finished, there will be a CSV output file 'ldap_out.csv' containing a list of computer objects. Run the nmap_enum script ($ python nmap_enum.py) which will identify all systems that have a running IPC$ share and will create a new CSV file 'nmap_out.csv' containing a list of IPs that can have the FireEye agent remotely deployed at that point of scanning (NOTE: you should only be scanning systems on your domain). After creating a list of deployable systems (nmap_out.csv) you are now ready to deploy the agent. Run the AgentCopy script ($ python agentCopy.py) and the 3 installation files will be copied to each system in the nmap_out.csv list. Finally, run the agentInstall script ($ python agentInstall.py) and the list of systems will have the agent installed. At this point check your management server for a list of FireEye agents communicating.
