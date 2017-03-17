#-*- coding: utf-8 -*-
import svnDiffParser, sys
import settings, differential
from phabricator import Phabricator 
from fabricatorTools.fab import getFab, getUsers
fab = getFab()

username = settings.USER['name']
password = settings.USER['password']

def createReviewRequest():
#    differential.createReviewRequest()
    pass

def getDiffRevision():
    print differential.getDiffRevision()

def testDifferential():
    differential.getReviewDifferential(username = username, password = password, rev = 1, fab = fab)

def testFab():
    ret = fab.differential.query(ids = [1])
    print ret

tests = {
    'differential': testDifferential,
    'fab': testFab,
    'diffReview': createReviewRequest,
    'getDiffRevision': getDiffRevision,
}

if __name__ == '__main__':
    try:
        test = tests[sys.argv[1]]
        try:
            test()
        except Exception, e:
            print e
    except Exception, e:
        print e
        for testName, test in tests.items():
            print 'testing:', testName
            test()

