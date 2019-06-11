from __future__ import print_function
from testlink import TestlinkAPIClient, TestLinkHelper, TestGenReporter
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
from testlink.testlinkerrors import TLResponseError
import sys, os.path
from platform import python_version
from unittest import (
    TestLoader,
    TextTestResult,
    TextTestRunner)
from pprint import pprint
import os


class AppDynamicsJob(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path='C:\Windows\chromedriver.exe')
        self.driver.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_app_dynamics_job(self):
        driver = self.driver
        driver.get("http://jaroslaw.rudy.staff.iiar.pwr.wroc.pl/dydaktyka.php")
        driver.find_element_by_id("sdizoC_button").click()
        driver.find_element_by_id("javaZ_button").click()
        driver.find_element_by_id("so2p_button").click()
        driver.find_element_by_id("so2l_button").click()
        self.successes = []

        def addSuccess(self, test):
            # addSuccess do nothing, so we need to overwrite it.
            super( AppDynamicsJob, self ).addSuccess( test )
            self.successes.append( test )

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()

            else:
                alert.dismiss()

            return alert_text
        finally:
            self.accept_next_alert = True

            def json_append(self, test, result, out):
                suite = test.__class__.__name__
                if suite not in out:
                    out[suite] = {OK: [], FAIL: [], ERROR: [], SKIP: []}
                if result is OK:
                    out[suite][OK].append( test._testMethodName )
                elif result is FAIL:
                    out[suite][FAIL].append( test._testMethodName )
                elif result is ERROR:
                    out[suite][ERROR].append( test._testMethodName )
                elif result is SKIP:
                    out[suite][SKIP].append( test._testMethodName )
                else:
                    raise KeyError( "No such result: {}".format( result ) )
                return out

            def jsonify(self):
                json_out = dict()
                for t in self.successes:
                    json_out = self.json_append( t, OK, json_out )

                for t, _ in self.failures:
                    json_out = self.json_append( t, FAIL, json_out )

                for t, _ in self.errors:
                    json_out = self.json_append( t, ERROR, json_out )

                for t, _ in self.skipped:
                    json_out = self.json_append( t, SKIP, json_out )

                return json_out

    def tearDown(self):
        self.assertEqual([], self.verificationErrors)


if __name__ == '__main__':
    # redirector default output of unittest to /dev/null
    with open( os.devnull, 'w' ) as null_stream:
        runner = TextTestRunner( stream=null_stream )
        runner.resultclass = AppDynamicsJob

        TESTLINK_API_PYTHON_SERVER_URL = 'http://127.0.0.1/testlink/lib/api/xmlrpc/v1/xmlrpc.php'
        #wpisz swój klucz w dół
        TESTLINK_API_PYTHON_DEVKEY = '724497bfde0cc05904c85a68a1263c6d'
        tl_helper = TestLinkHelper(TESTLINK_API_PYTHON_SERVER_URL, TESTLINK_API_PYTHON_DEVKEY)
        myTestLink = tl_helper.connect(TestlinkAPIClient)
        print(myTestLink.connectionInfo())

        print(myTestLink.countProjects())
        tc_info = myTestLink.getTestCase(None, testcaseexternalid='26-2')
        print(tc_info)
        tc_info = myTestLink.getProjectTestPlans('1')
        print(tc_info)
        # tls.reportTCResult(4, 2, 'SampleBuild', 'f', 'some notes', user='user', platformid='1')
        myTestLink.reportTCResult(None, 2, None, 'p', 'some notes', guess=True,
                           testcaseexternalid='26-2',
                           platformname='DPP',
                           execduration=3.9, timestamp='2020-06-10 12:03',
                           steps=[{'step_number': 1, 'result': 'p', 'notes': 'result note for passed step 1'}])