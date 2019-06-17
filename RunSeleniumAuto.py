#RunSeleniumAuto.py

import getopt, os, sys
from SeleniumAuto import *
#
#=====================================Variable Declarations==============================================================================
global SAObj
#========================================================================================================================================
def EvaluateArgs():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:s:n:", ["help", "file=", "server=", "name="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)
        Usage()
        sys.exit(2)

    Cfg_given=False
    Sec_given=False
    Srv_given=False
	
    for o, a in opts:
        if o in ("-n", "--name"):
            Sec_given=True
            print('Section heading under which Java commands live is %s ' % a )
            SAObj.Set_Section_Heading(a)
            SecHeading=a
            
        elif o in ("-s", "--server"):
            Srv_given=True
            print('Target server specified is %s ' % a )
            SAObj.Set_Host_Name(a)
            
        elif o in ("-f", "--file"):
            Cfg_given=True
            print('Setting QA Operations Config file to : %s ' %  a )
            SAObj.Set_Config_File(a)
            
        elif o in ("-h", "--help"):
            Usage()
            sys.exit()
        else:
            assert False, "Unhandled option."
	
    if False in (Cfg_given, Sec_given, Srv_given):
        print("ERROR: One of the mandatory parameters is missing. Must specify mandatory parameters.")
        Usage()
        sys.exit(2)
            
#========================================================================================================================================
def Usage():
    print("Usage:")
    print("\n%s -f Config_File -n Section_Heading -s Target_Server"  % sys.argv[0])
    print("%s --file Config_File --name Section_Heading --server Target_Server"  % sys.argv[0])
    print("\nConfig_File is the Configuration File. Section_Heading is the name or label of the section that contains data.")
    print("Target_Server is the host on which tests are going to be executed.")
    print("\nConfig file , Target Server host name and Section Heading name (both must be as is in the config file) are mandatory options.") 
   
#========================================================================================================================================

if __name__ == "__main__":
    SAObj=SeleniumAuto()
    #
    EvaluateArgs()
    print(sys.argv)
    
    SAObj.Set_Host_Config_Dict()
   
    SAObj.Set_Config_Dict()
    #SAObj.Set_Contact_IpAddr(SAObj.CONFIG['IPAddr'])
    SAObj.Set_TLO_Object()
    #SAObj.GetTCEResult('C:\PyHeaven\RunSeleAuto\ev1111.out')
    SAObj.ExecuteCommands()
    