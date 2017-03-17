#-*- coding: utf-8 -*-
import settings
import requests, sys, re, os.path
from fabricatorTools.fab import getFab, getUsers
from fabricatorTools.userMock import FabMock
fabDefault = getFab()

def getReviewDifferential(**args):
    username = args.pop('username', settings.USER['name'])
    password = args.pop('password', settings.USER['password'])
    rev = args.pop('rev', None)
    fab = args.pop('fab', fabDefault)
    uri = args.pop('uri', ur"http://192.168.99.100:8001/D2")
    diffTargetName = os.path.basename(uri)
    diffDirName = os.path.dirname(uri)
    session = requests.Session()
    mock = FabMock()
    resp = session.get(settings.SITE["URL"])
    token = mock.getCsrfValue(resp.text)
    resp = mock.login(username = username, password = password, csrfToken = token, session = session)
    resp = session.get(uri)
    p = re.compile(ur'href="/({dname}[^"]+download=true")'.format(dname = diffTargetName))
    m = p.search(resp.text)
    rawDiffPath = os.path.join(diffDirName, m.groups()[0])
    resp = session.get(rawDiffPath)
    if resp.status_code != 200:
        return ""
    return resp.text

def getDiffRevision(**args):
    username = args.pop('username', settings.USER['name'])
    password = args.pop('password', settings.USER['password'])
    rev = args.pop('rev', None)
    fab = args.pop('fab', fabDefault)
    uri = args.pop('uri', ur"http://192.168.99.100:8001/D2")
    diffTargetName = os.path.basename(uri)
    diffDirName = os.path.dirname(uri)
    resp = fab.phid.lookup(names = [diffTargetName])
    return resp.response[diffTargetName]
