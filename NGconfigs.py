#!/usr/bin/python
#    Program:  NGconfigs
#  
#    Date:  March 9, 2016
#
#    Programmer:  Rob Moore
#
#    Purpose:   Generate network equipment configurations for NextGen stores
#
#    Input:     Route template configurations
#               /home/af003/storetemplates/NGroutertemplate.txt
#              
#
#    Output:   NextGen store router config
#              /home/af003/storeconfigs/ + storeno + router.txt
############################################################################## 
import time
import subprocess

############################################################################## 
#   Tempalate File
############################################################################## 
routertemplate = "/home/af003/storetemplates/NGroutertemplate.txt"



############################################################################## 
#    Define router info needed
############################################################################## 
class router():
 
    #####################################################################
   	# Function: __init__ 
	#
	# Purpose:  Initialize Variables
	#
	# Variables:  store               Store number
	#             subnet              Whole store subnet
	#             HHRange             Range for Handhelds
	#             LaptopRange         Range for Laptops
	#             APRange             Range for APs
	#             WirelessPhoneRange  Range for Wireless Phones
	#             WiredPhoneRange     Range for Wired Phones
	#             LegacyWirelessRange Range for Legacy Wireless
	#
	# Parameters: store_subnet         Subnet of store
	#
	# Return Value: None
	######################################################################
    def __init__(self, stono, subnet, circuit, wan):
        self.store =  stono.strip()
        self.storesubnet = subnet
        self.circuitid = circuit
        self.wanip  = wan
        self.subnet2 = ""
        self.subnet3 = ""
        self.subnet3_1 = ""
        self.subnet3_2 = ""
        self.subnet3_3 = ""
        self.bgppeer = ""
        self.nzstore = ""

    #####################################################################
   	# Function:     Ranges
	#
    # Purpose:      Generate all the DHCP ranges for NextGen stores
	#
	# Variables:    None
	#
	# Parameters:  outfile           Output file to write ranges 
    #
	# Return Value: SSH_Output       None
	######################################################################
    def genvalues(self):
    
        Storesubnets = self.storesubnet.split('.')
        self.subnet2 = Storesubnets[1]
        self.subnet3 = Storesubnets[2]
        self.subnet3_1 = str(int(self.subnet3) + 1)
        self.subnet3_2 = str(int(self.subnet3) + 2)
        self.subnet3_3 = str(int(self.subnet3) + 3)
        StoreWANIP = self.wanip.split('.')
        StoreWANIP[3] = str(int(StoreWANIP[3]) - 1)
        self.bgppeer = '.'.join(StoreWANIP)
        self.nzstore = self.store.lstrip('0')
		
		
    #####################################################################
   	# Function:     Ranges
	#
    # Purpose:      Generate all the DHCP ranges for NextGen stores
	#
	# Variables:    None
	#
	# Parameters:  outfile           Output file to write ranges 
    #
	# Return Value: SSH_Output       None
	######################################################################
    def updatetemplate(self,templine):
    
        templine = templine.replace("[storenumber]",self.store)
        templine = templine.replace("[x]",self.subnet2)
        templine = templine.replace("[y]",self.subnet3)
        templine = templine.replace("[y+1]",self.subnet3_1)
        templine = templine.replace("[y+2]",self.subnet3_2)
        templine = templine.replace("[y+3]",self.subnet3_3)
        templine = templine.replace("[cir-id]",self.circuitid)
        templine = templine.replace("[wanip]",self.wanip)
        templine = templine.replace("[nz-storenumber]",self.nzstore)
        templine = templine.replace("[bgp_peer]",self.bgppeer)

        
        return(templine)

		
			   
#####################################################################
# Function:     main
#
# Purpose:      Main Program
#
# Variables:    None
#
# Parameters:   None
#
# Return Value: None
#######################################################################	
def main():
    
	#  Get input to generate config
    storeno = raw_input("Storeno: ")
    storesub = raw_input("Store Subnet: ")
    circuitid = raw_input("CircuitID: ")
    wanip = raw_input("WAN IP: ")
	
    routerobj = router(storeno, storesub, circuitid, wanip)
    routerobj.genvalues()

    #  Open output file which will have ranges
    routerconfig =  "/home/af003/storeconfigs/" + storeno + "router.txt"
    configf = open(routerconfig,'w')

    #  Pull in each store in NextGen store file
    with open(routertemplate,'r') as templatef:
        templatelines = templatef.read().splitlines(True)
	
    #  Process each store to get DHCP ranges	
    for configline in templatelines:
        updatedline = routerobj.updatetemplate(configline)
        configf.write(updatedline + "\n")
    print ("Config file writtenn as " + storeno + "router.txt")
    configf.close()
    templatef.close()
                
	
if __name__ == '__main__': main()
