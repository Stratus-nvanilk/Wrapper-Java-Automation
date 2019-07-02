#Name:SeleniumAuto Class.
#Description: This class is a part of the wrapper program that drives Selenium/Java Automation
#by Augmentum. This file encapsulates methods and data structures required by the wrapper.
#Initial Developer: N.V. Anil Kumar
#Company: Stratus Technologies, MA,USA
#Date : 2-July-2019
#===============================================================================================

import getopt, os, sys, fileinput, time, pprint
import logging
from socket import gethostname
from TestLinkOps import *

#---------------------------------------------
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
        
    def Set_Batch_Config_Dict(self):
        self.BATCH_CONFIG=CL.GetDFSec2Dict(self.CONFIG_FILE, self.SECTION_HEADING)
        print('\nBATCH_CONFIG dictionary is now loaded with keys and values from CONFIG file...')
        print('\nContents of BATCH_CONFIG dictionary : ')
        pprint.pprint(self.BATCH_CONFIG)

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
        Target_Log_Dir=self.CONFIG['EXEC_LOG_DIR'] if self.CONFIG.get('EXEC_LOG_DIR') else CL.CWD
        Ordered_List=self.CONFIG['EXEC_ORDER'].split(',')
        #
        for TC in Ordered_List:
            print("\nTest Case %s --- Commencing Execution" % TC)
            TestOut=CL.Create_DestDir_Join_Filename(Target_Log_Dir,TC+".out")
            TestErr=CL.Create_DestDir_Join_Filename(Target_Log_Dir,TC+".err")
            Ofile= open(TestOut,"w+")
            Efile= open(TestErr,"w+")
            print('Executing the following command line of the test case %s : ' % TC)
            print(self.CONFIG[TC])
            CL.RunCMD(self.CONFIG[TC], outfile=Ofile, errfile=Efile)
            Ofile.close()
            Efile.close()
            TCEResult=self.GetTCEResult(TestOut)
            if TCEResult:            
                self.UpdateTestLink(TC,TCEResult)
            elif not TCEResult:
                print("Test Case execution status seems to be invalid! Skipping TestLink updation for this test case : %s " % TC)
            print("\nTest Case %s --- End of Execution" % TC)    
            print("\n=========================================================================================================================\n")
    
    def Process_SectionHeading(self, SecHeading):
        print("Processing Section heading : %s " % SecHeading)
        self.Set_Section_Heading(SecHeading)
        self.Set_Config_Dict()
        self.ExecuteCommands()
        
    def Process_SH_Batch(self, SecHeading):
        print("Execution in Batch Processing Mode.")
        print("Processing one by one all the section headings found under section of sections : %s " % SecHeading)
        Ordered_List=self.BATCH_CONFIG['EXEC_ORDER'].split(',')
        #
        for key in Ordered_List:
            SH=self.BATCH_CONFIG[key]
            self.Process_SectionHeading(SH)
        
            