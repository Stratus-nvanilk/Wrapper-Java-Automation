#SeleniumAuto Class.

import getopt, os, sys, fileinput, time, pprint
#import paramiko
import logging
from socket import gethostname
from TestLinkOps import *

#---------------------------------------------
#import SSHOps
import CommonLibrary as CL

class SeleniumAuto():
    # Variable declarations:
    #
    OSPLATFORM=sys.platform
    CONFIG = {}
    HOST_CONFIG = {}
    CONFIG_FILE = r""
    TARGET_HOST = ""
    CONTACT_IPADDR = ""
    SECTION_HEADING=""
    TLOObj=""
           
#=======================================================================================================================
    def __init__(self):
        print("Creating an object of SeleniumAuto...")
        return None

    def Set_Config_File(self,FileName): 
        print("----->" + FileName)
        print('CONFIG_FILE' + ' is now set to ' + FileName)
        self.CONFIG_FILE=FileName

    def Set_Host_Name(self,HostName):
        print("----->" + HostName)
        self.TARGET_HOST=HostName
        print('TARGET_HOST' + ' is now set to %s ' % self.TARGET_HOST)

    def Set_Section_Heading(self,SecName):
        print("----->" + SecName)
        self.SECTION_HEADING=SecName
        print('SECTION_HEADING' + ' is now set to %s ' % self.SECTION_HEADING)
    
    def Set_Host_Config_Dict(self):
        self.HOST_CONFIG=CL.GetDFSec2Dict(self.CONFIG_FILE, self.TARGET_HOST)
        print('\nHOST_CONFIG dictionary is now loaded with keys and values from CONFIG file...')
        print('\nContents of HOST_CONFIG dictionary : ')
        pprint.pprint(self.HOST_CONFIG)
        
    def Set_Config_Dict(self):
        self.CONFIG=CL.GetDFSec2Dict(self.CONFIG_FILE, self.SECTION_HEADING)
        print('\nCONFIG dictionary is now loaded with keys and values from CONFIG file...')
        print('\nContents of CONFIG dictionary : ')
        pprint.pprint(self.CONFIG)
        
    # def Set_Contact_IpAddr(self):
        # self.CONTACT_IPADDR = self.HOST_CONFIG['IPAddr']
        # print('\nCONTACT_IPADDR is now set to %s ' %  self.CONTACT_IPADDR)

    def Set_Contact_IpAddr(self, IPAddr=None):
        self.CONTACT_IPADDR = IPAddr
        print('CONTACT_IPADDR is now set to %s ' %  self.CONTACT_IPADDR)
        
    def Get_TLO_Object(self):
        TLOObjectName=TestLinkOps()
        return TLOObjectName
        
    def Set_TLO_Object(self):
        print('Obtaining a TestLink Operations Object and assigning it to a holder...')
        self.TLOObj=self.Get_TLO_Object()
        print("Done.")
        
    def GetTCEResult(self,OutputFile):
        TCEResult=""
        print("Searching for Test Execution Result in the output file %s " % OutputFile)
        with open(OutputFile) as fp:  
            line = fp.readline()
            while line:
                line=line.strip()
                if line.endswith("PASS"):
                    TCEResult='p'
                elif line.endswith("FAIL"):
                    TCEResult='f'                
                line = fp.readline()
        print("Test Execution Result is determined as : %s " % TCEResult)
        return TCEResult
        
    def UpdateTestLink(self,TCName,TCEResult):
        print("Preparing to update test case execution results directly on TestLink application...")
        TCData={key:self.HOST_CONFIG[key] for key in self.HOST_CONFIG.keys() & {'TesterName', 'TestPlanID', 'BuildName', 'PlatformID', 'TestNotes'}}
        TCData['TestCaseID']=TCName
        TCData['TCEResult']=TCEResult
        TC_Info=self.TLOObj.ReportTestResult(**TCData)
        pprint.pprint(TC_Info)
                        
    def ExecuteCommands(self):
        Ordered_List=self.CONFIG['EXEC_ORDER'].split(',')
        for TC in Ordered_List:
            TestOut=TC+".out"
            TestErr=TC+".err"
            Ofile= open(TestOut,"w+")
            Efile= open(TestErr,"w+")
            print('Executing the following command line of the test case %s : ' % TC)
            print(self.CONFIG[TC])
            CL.RunCMD(self.CONFIG[TC], outfile=Ofile, errfile=Efile)
            Ofile.close()
            Efile.close()
            TCEResult=self.GetTCEResult(TestOut)
            self.UpdateTestLink(TC,TCEResult)

            