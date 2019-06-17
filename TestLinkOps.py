#TestLinkOps.py
from __future__ import print_function
import testlink
from testlink import TestlinkAPIClient, TestLinkHelper, TestGenReporter
from testlink.testlinkerrors import TLResponseError
from platform import python_version
import CommonLibrary as CL  
#=======================================================================================================
class TestLinkOps :
    # Variable declarations:
    TESTLINK_API_PYTHON_SERVER_URL='http://is-qa2.sw.stratus.com/testlink/lib/api/xmlrpc/v1/xmlrpc.php'
    TESTLINK_API_PYTHON_DEVKEY='2075d5aefb74617ddb86df9176bc690f'
    TLO=None

    def __init__(self, server_url=None, devkey=None, proxy=None):
        print("Creating a Test object to work with TestLink Operations...")       
        self.TLO=self.GetTLAPIClient()
        return
        
    def GetTLAPIClient(self):
        print("Creating a TestLink API Client object to help work with TestLink Operations...")
        print("Server URL used : %s "  %  self.TESTLINK_API_PYTHON_SERVER_URL)
        print("Using the hardcoded Dev key for authorization...") 
        TestLinkObj= testlink.TestLinkHelper(server_url=self.TESTLINK_API_PYTHON_SERVER_URL, devkey=self.TESTLINK_API_PYTHON_DEVKEY).connect(testlink.TestlinkAPIClient)
        return TestLinkObj
    
    def GetTestCaseInfo(self,TCExtID):
        print("Fetching details of test case with Test Case external ID %s from TestLink..." % TCExtID)
        TC_Info=self.TLO.getTestCase(None,testcaseexternalid=TCExtID)
        return TC_Info
        
    def ReportTestResult(self, **TCData):
        TestCaseID=TCData['TestCaseID']
        TestPlanID=TCData['TestPlanID']
        BuildName=TCData['BuildName']
        TCEResult=TCData['TCEResult']
        PlatformID=TCData['PlatformID']
        TestNotes=TCData['TestNotes']
        TesterName=TCData['TesterName']
        print("Updating the result of test execution on Test Link using the following execution data:")
        print(TCData)
        TC_Info=self.TLO.reportTCResult(testplanid=TestPlanID, status=TCEResult, testcaseexternalid=TestCaseID, buildname=BuildName, notes=TestNotes, user=TesterName, platformid=PlatformID)
        return TC_Info               

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#Personal API Access Key = 3e8d34447eabe0773ee11c32f2d7e652

# tls = testlink.TestLinkHelper().connect(testlink.TestlinkAPIClient)
# tls.countProjects()

# tc_info = tls.getTestCase(None, testcaseexternalid='eE-2815')
