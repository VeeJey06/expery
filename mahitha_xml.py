#!/usr/bin/env python
# -*- encoding:utf-8-*-
# -*- coding: utf-8 -*-

#import sys
import os
import datetime
import requests, json
import xml.etree.cElementTree as ET


#AZURE
APIURL="https://prod-02.koreacentral.logic.azure.com:443/workflows/79f1422c2a4e4d5a91940602473ec989/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=i3cXwN0aSgXVYdCJ5J9EWERfKsvdYmZaRqL42UrLKEQ"
#FLOW
#APIURL="https://prod-142.westus.logic.azure.com:443/workflows/0162b7aeb22a4e5b85c56835c0d5193d/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=BWQF1BPjdTwkq9QM16-jFcPGev0VdiqAobJoZY-XmOE"

def printLines():
    print("=" * 80)

from optparse import OptionParser
from robot.api import ExecutionResult, SuiteVisitor
from robot.errors import DataError

class PrintTestInfo(SuiteVisitor):
    def visit_test(self, test):
        print('{:40s} | {} | {:7d} | {}'.format(test.name, test.starttime,
                                         test.elapsedtime, test.status))

class PrintSuiteInfo(SuiteVisitor):
    def visit_suite(self, suite):
        print('{:40s} | {} | {:7d} | {}'.format(suite.name, suite.starttime,
                                         suite.elapsedtime, suite.status))

def parse_gfriend_results(path):
    outxml = ET.parse(path)

    test_result = {}
    root = outxml.getroot()
    print("Suite Name:", root.attrib['Name'])

    total =  0
    pass_count = 0
    fail_count = 0
    for r in root.iter('Result'):
        total +=1
        if 'pass' in r.text.strip().casefold():
            pass_count += 1
        elif 'fail' in r.text.strip().casefold():
            fail_count += 1
    ts_start = datetime.datetime.strptime(root.find('StartTime').text.strip(), '%Y-%m-%d %H:%M:%S')
    ts_end = datetime.datetime.strptime(root.find('EndTime').text.strip(), '%Y-%m-%d %H:%M:%S')
    test_result['ts_start'] = ts_start.strftime("%Y-%m-%d %H:%M:%S")
    test_result['ts_end'] = ts_end.strftime("%Y-%m-%d %H:%M:%S")
    test_result['result.passrate'] = '%2.1f%%' % (pass_count * 100 / total)
    test_result['result.count.total'] = total
    test_result['result.count.passed'] = pass_count
    test_result['result.count.failed'] = fail_count
    # Naming Rule 없음. IPT는 L2에서 추적하고, WF는 L3까지 개별 TC를 추적함.
    test_result['testsuite.lv3'] = root.attrib['Name'].strip()

    return test_result

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--output", dest="output",
                  help="full path of output.xml",type='string',
                  default="")
    parser.add_option("--posturl", dest="url",
                  help="url to post result",type='string',
                  default="https://prod-29.koreacentral.logic.azure.com:443/workflows/14b04fa9ea2c4479b5eda8bf29d43dc4/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=d1tAy8Xlkis3l7hQBZGj0BhD6lrPqnWfMluXK61IG34")
    parser.add_option("--tsuitelv1", dest="tsuitelv1", help="WF, IPT, JRNY ", type='string', default="JRNY")
    parser.add_option("--tsuitelv2", dest="tsuitelv2", help="JRNY Placeholder1/2/3", type='string', default="JRNY")
    parser.add_option("--stack", dest="stack",help="stack : PROD, STG",type='string',default="PROD")
    parser.add_option("--prdkey", dest="prdkey", help="Key of the DUT", type='string', default="")
    parser.add_option("--dutid", dest="dutid", help="ID of the DUT:LTL-20773: Busch MT1,LTL-12831: Cordoba", type='string', default="")
    parser.add_option("--fwversion", dest="fwversion", help="Firmware Verison of the DUT", type='string', default="")
    parser.add_option("--tlocation", dest="tlocation", help="Test Location: 1(Mphasis Bangalore), 2(Mphasis Boise),6(BYS Beijing),7(BYS Wuhan),11(SIV US),12(SIV Singapore),13(SIV Korea),14(RCB Bangalore)",
                      type='string', default="1")
    parser.add_option("--sessionid", dest="sessionid", help="Session ID", type='string', default="")
    parser.add_option("--buildurl", dest="buildurl", help="Build URL", type='string', default="")
    parser.add_option("--telesend", dest="telesend", help="send result to telegram", type='string', default="")
    parser.add_option("--jobname", dest="jobname", help="job name", type='string', default="")
    parser.add_option("--skiptocallhttp", dest="skiptocallhttp", help="skip to call http", type='string', default="")
    (options, args) = parser.parse_args()

    if os.path.exists(options.output):
        testresult = {}
        try:
            result = ExecutionResult(options.output)
        except DataError:
            testresult = parse_gfriend_results(options.output)
        else:
            printLines()
            print("Case Result")
            printLines()
            result.suite.visit(PrintTestInfo())
            printLines()
            print("Suite Result")
            printLines()
            result.suite.visit(PrintSuiteInfo())
            printLines()
            ts_start = datetime.datetime.strptime(result.suite.starttime, '%Y%m%d %H:%M:%S.%f')
            ts_end = datetime.datetime.strptime(result.suite.endtime, '%Y%m%d %H:%M:%S.%f')
            testresult['ts_start'] = ts_start.strftime("%Y-%m-%d %H:%M:%S")
            testresult['ts_end'] = ts_end.strftime("%Y-%m-%d %H:%M:%S")
            testresult['result.passrate'] = '%2.1f%%' % (result.suite.statistics.all.passed * 100 / result.suite.statistics.all.total)
            testresult['result.count.total'] = result.suite.statistics.all.total
            testresult['result.count.passed'] = result.suite.statistics.all.passed
            testresult['result.count.failed'] = result.suite.statistics.all.failed
            # Naming Rule 없음. IPT는 L2에서 추적하고, WF는 L3까지 개별 TC를 추적함.
            testresult['testsuite.lv3'] = result.suite.name


        version = ''
        if os.environ.get('FWREVISION'):
            version = os.environ['FWREVISION']
        if len(options.fwversion) > len(version):
            version = options.fwversion
        testresult['testsuite.lv1'] = options.tsuitelv1
        testresult['testsuite.lv2'] = options.tsuitelv2
        # 고유값 필요
        testresult['run.session.id'] = options.sessionid
        testresult['config.stack'] = options.stack
        testresult['config.productkey'] = options.prdkey
        testresult['config.dutid'] = options.dutid
        testresult['config.fwversion'] = version
        testresult['info.locaiton'] = options.tlocation

        buildurl = ''
        if os.environ.get('BUILD_URL'):
            buildurl = os.environ['BUILD_URL']
        if len(options.buildurl) > len(buildurl):
            buildurl = options.buildurl
        testresult['dispatcher'] = buildurl

        print(json.dumps(testresult))

        if options.skiptocallhttp.lower().find("skip") >= 0:
            print("skiptocallhttp")
            pass
        else:
            resp = requests.post(options.url,data=json.dumps(testresult),headers={'Content-Type': 'application/json'})

        # print("suite status:", result.suite.status)
        if options.telesend.lower().find("on") >= 0:
            jobname = ''
            if len(options.jobname):
                jobname = options.jobname
            elif os.environ.get('JOB_NAME'):
                jobname = os.environ['JOB_NAME']

            os.system('telegram-send --config eSRVT\\group1.conf "%s %s"' % (jobname, result.suite.status))

